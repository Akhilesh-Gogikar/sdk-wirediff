#!/usr/bin/env python3
"""Deterministic cross-SDK semantic observation diff (standard library only)."""

from __future__ import annotations

import argparse
import copy
import html
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
from urllib.parse import parse_qs, urlsplit


SCHEMA_VERSION = 1
MAX_INPUT_BYTES = 2 * 1024 * 1024
REQUIRED_ADAPTERS = ("typescript", "python", "go")
CATEGORIES = ("defaults", "errors", "retries", "pagination", "nulls", "fields")
MISSING = object()


class WireDiffError(Exception):
    """A concise, user-actionable manifest or observation error."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def read_json(path: Path) -> Any:
    try:
        if path.stat().st_size > MAX_INPUT_BYTES:
            raise WireDiffError(f"input exceeds 2 MiB: {path}")
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except WireDiffError:
        raise
    except (OSError, json.JSONDecodeError) as error:
        raise WireDiffError(f"cannot read JSON {path}: {error}") from error


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def json_body(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if not stripped.startswith(("{", "[")):
        return value
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return value


def normalized_headers(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise WireDiffError("HTTP headers must be an object")
    sensitive = {"authorization", "proxy-authorization", "cookie", "set-cookie", "x-api-key"}
    return {
        str(key).lower(): "[REDACTED]" if str(key).lower() in sensitive else str(item).strip()
        for key, item in sorted(value.items(), key=lambda pair: str(pair[0]).lower())
    }


def normalized_query(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise WireDiffError("request.query must be an object")
    output: dict[str, Any] = {}
    for key in sorted(value, key=str):
        item = value[key]
        lowered = str(key).lower().replace("-", "_")
        if lowered in {"api_key", "access_token", "token", "secret", "password", "signature"}:
            output[str(key)] = "[REDACTED]"
        elif isinstance(item, list):
            output[str(key)] = [str(entry) for entry in item]
        elif item is None:
            output[str(key)] = None
        else:
            output[str(key)] = str(item)
    return output


def normalize_observation(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise WireDiffError("each observation must be a JSON object")
    output = copy.deepcopy(raw)

    request = output.get("request") or {}
    if not isinstance(request, dict):
        raise WireDiffError("observation.request must be an object")
    request = copy.deepcopy(request)
    if "method" in request:
        request["method"] = str(request["method"]).upper()
    request["headers"] = normalized_headers(request.get("headers"))
    if isinstance(request.get("url"), str):
        parsed = urlsplit(request["url"])
        request.setdefault("path", parsed.path or "/")
        if "query" not in request:
            query = parse_qs(parsed.query, keep_blank_values=True)
            request["query"] = {key: values[0] if len(values) == 1 else values for key, values in sorted(query.items())}
        request.pop("url", None)
    request["query"] = normalized_query(request.get("query"))
    if "body" in request:
        request["body"] = json_body(request["body"])
    output["request"] = request

    response = output.get("response") or {}
    if not isinstance(response, dict):
        raise WireDiffError("observation.response must be an object")
    response = copy.deepcopy(response)
    if "status" not in response and "status_code" in response:
        response["status"] = response.pop("status_code")
    if "status" in response:
        try:
            response["status"] = int(response["status"])
        except (TypeError, ValueError) as error:
            raise WireDiffError("response.status must be an integer") from error
    response["headers"] = normalized_headers(response.get("headers"))
    if "body" in response:
        response["body"] = json_body(response["body"])
    output["response"] = response

    attempts = output.get("attempts", [])
    if not isinstance(attempts, list):
        raise WireDiffError("observation.attempts must be an array")
    output["attempts"] = attempts

    error_value = output.get("error", MISSING)
    if error_value is MISSING and response.get("status", 0) >= 400 and isinstance(response.get("body"), dict):
        error_value = response["body"].get("error", MISSING)
    if error_value is not MISSING:
        output["error"] = {"message": error_value} if isinstance(error_value, str) else error_value

    if "pagination" not in output:
        pagination: dict[str, Any] = {}
        body = response.get("body")
        if isinstance(body, dict):
            for candidate in ("next_cursor", "next_token", "next"):
                if candidate in body:
                    pagination["next"] = body[candidate]
                    break
            for candidate in ("items", "data"):
                if isinstance(body.get(candidate), list):
                    pagination["items_count"] = len(body[candidate])
                    break
        output["pagination"] = pagination
    elif not isinstance(output["pagination"], dict):
        raise WireDiffError("observation.pagination must be an object")
    return output


def pointer_get(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise WireDiffError(f"probe path must be an RFC 6901 JSON pointer: {pointer!r}")
    current = value
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                return MISSING
            current = current[token]
        elif isinstance(current, list):
            try:
                index = int(token)
            except ValueError:
                return MISSING
            if index < 0 or index >= len(current):
                return MISSING
            current = current[index]
        else:
            return MISSING
    return current


def missing_value() -> dict[str, str]:
    return {"state": "missing"}


def transform_value(value: Any, transform: str, label: str) -> Any:
    if transform == "presence":
        if value is MISSING:
            return {"state": "missing"}
        if value is None:
            return {"state": "null"}
        return {"state": "value", "type": type(value).__name__}
    if value is MISSING:
        return missing_value()
    if transform == "identity":
        return value
    if transform == "length":
        if not isinstance(value, (dict, list, str)):
            raise WireDiffError(f"probe {label} cannot take length of {type(value).__name__}")
        return len(value)
    if transform == "keys":
        if not isinstance(value, dict):
            raise WireDiffError(f"probe {label} expected an object for keys transform")
        return sorted(str(key) for key in value)
    if transform == "sorted":
        if not isinstance(value, list):
            raise WireDiffError(f"probe {label} expected an array for sorted transform")
        return sorted(value, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    if transform == "status-class":
        if not isinstance(value, int):
            raise WireDiffError(f"probe {label} expected an integer status")
        return f"{value // 100}xx"
    raise WireDiffError(f"probe {label} has unsupported transform {transform!r}")


def normalize_probes(observation: dict[str, Any], compare: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(compare, dict):
        raise WireDiffError("manifest.compare must be an object")
    unknown = set(compare) - set(CATEGORIES)
    if unknown:
        raise WireDiffError(f"unknown comparison categories: {', '.join(sorted(unknown))}")
    semantics: dict[str, dict[str, Any]] = {}
    for category in CATEGORIES:
        probes = compare.get(category, {})
        if not isinstance(probes, dict):
            raise WireDiffError(f"compare.{category} must be an object")
        semantics[category] = {}
        for name in sorted(probes):
            raw_spec = probes[name]
            spec = {"path": raw_spec} if isinstance(raw_spec, str) else raw_spec
            if not isinstance(spec, dict) or not isinstance(spec.get("path"), str):
                raise WireDiffError(f"compare.{category}.{name} needs a path")
            transform = str(spec.get("transform", "identity"))
            value = pointer_get(observation, spec["path"])
            semantics[category][name] = transform_value(value, transform, f"{category}.{name}")
    return semantics


def load_adapter(name: str, spec: Any, base_dir: Path, allow_command: bool) -> tuple[dict[str, Any], dict[str, str]]:
    if not isinstance(spec, dict):
        raise WireDiffError(f"adapter {name} must be an object")
    modes = [mode for mode in ("observation", "command", "inline") if mode in spec]
    if len(modes) != 1:
        raise WireDiffError(f"adapter {name} needs exactly one of observation, command, or inline")
    mode = modes[0]
    if mode == "observation":
        relative = spec["observation"]
        if not isinstance(relative, str) or not relative:
            raise WireDiffError(f"adapter {name} observation must be a path")
        raw = read_json((base_dir / relative).resolve())
        return normalize_observation(raw), {"kind": "file", "value": relative}
    if mode == "inline":
        return normalize_observation(spec["inline"]), {"kind": "inline", "value": "manifest"}
    if not allow_command:
        raise WireDiffError(f"adapter {name} uses a command; pass --allow-command for trusted fixtures")
    argv = spec["command"]
    if not isinstance(argv, list) or not argv or not all(isinstance(item, str) and item for item in argv):
        raise WireDiffError(f"adapter {name} command must be a non-empty argv string array")
    argv = [sys.executable if item == "{python}" else item for item in argv]
    timeout = spec.get("timeoutSeconds", 10)
    if not isinstance(timeout, (int, float)) or timeout <= 0 or timeout > 300:
        raise WireDiffError(f"adapter {name} timeoutSeconds must be in (0, 300]")
    raw_env = spec.get("env", {})
    if not isinstance(raw_env, dict):
        raise WireDiffError(f"adapter {name} env must be an object")
    try:
        completed = subprocess.run(
            argv,
            cwd=base_dir,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, **{str(key): str(value) for key, value in raw_env.items()}},
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise WireDiffError(f"adapter {name} command failed to run: {error}") from error
    if completed.returncode != 0:
        message = completed.stderr[-1000:].strip()
        raise WireDiffError(f"adapter {name} command exited {completed.returncode}: {message}")
    if len(completed.stdout.encode("utf-8")) > MAX_INPUT_BYTES:
        raise WireDiffError(f"adapter {name} command output exceeds 2 MiB")
    try:
        raw = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise WireDiffError(f"adapter {name} command stdout is not one JSON object: {error}") from error
    return normalize_observation(raw), {"kind": "command", "value": f"{spec['command'][0]} ({len(spec['command'])} argv)"}


def compare_manifest(manifest_path: Path | str, allow_command: bool = False) -> dict[str, Any]:
    path_value = Path(manifest_path).resolve()
    manifest = read_json(path_value)
    if not isinstance(manifest, dict):
        raise WireDiffError("manifest must be a JSON object")
    adapters_spec = manifest.get("adapters")
    # ponytail: v0 keeps a fixed three-language matrix; general adapter plugins
    # can replace this guard when a fourth implementation has a proof fixture.
    if not isinstance(adapters_spec, dict) or set(adapters_spec) != set(REQUIRED_ADAPTERS):
        raise WireDiffError("v0 requires exactly typescript, python, and go adapters")
    baseline = manifest.get("baseline", "typescript")
    if baseline not in REQUIRED_ADAPTERS:
        raise WireDiffError("baseline must be typescript, python, or go")
    compare = manifest.get("compare")

    adapters: dict[str, Any] = {}
    for name in REQUIRED_ADAPTERS:
        normalized, source = load_adapter(name, adapters_spec[name], path_value.parent, allow_command)
        adapters[name] = {
            "source": source,
            "normalized": normalized,
            "semantics": normalize_probes(normalized, compare),
        }

    diffs: list[dict[str, Any]] = []
    baseline_semantics = adapters[baseline]["semantics"]
    for category in CATEGORIES:
        for probe in sorted(baseline_semantics[category]):
            expected = baseline_semantics[category][probe]
            for adapter in REQUIRED_ADAPTERS:
                if adapter == baseline:
                    continue
                actual = adapters[adapter]["semantics"][category][probe]
                if actual != expected:
                    diffs.append({
                        "category": category,
                        "probe": probe,
                        "baselineAdapter": baseline,
                        "baselineValue": expected,
                        "adapter": adapter,
                        "value": actual,
                    })
    categories = sorted({item["category"] for item in diffs})
    return {
        "schemaVersion": SCHEMA_VERSION,
        "name": str(manifest.get("name", path_value.stem)),
        "baseline": baseline,
        "adapters": adapters,
        "diffs": diffs,
        "summary": {
            "adapterCount": len(adapters),
            "divergenceCount": len(diffs),
            "divergentCategories": categories,
        },
    }


def minimal_repro(result: dict[str, Any]) -> dict[str, Any]:
    compare: dict[str, dict[str, dict[str, str]]] = {}
    # The result semantics no longer carries source pointers, so compare the
    # compact semantic values directly in inline observations.
    divergent = {(item["category"], item["probe"]) for item in result["diffs"]}
    for category, probe in sorted(divergent):
        compare.setdefault(category, {})[probe] = f"/semantics/{category}/{probe}"
    adapters = {}
    involved = {result["baseline"], *(item["adapter"] for item in result["diffs"])}
    for name in REQUIRED_ADAPTERS:
        semantics = result["adapters"][name]["semantics"]
        # v0 manifests require all three language slots; uninvolved slots use
        # the baseline semantics so the repro cannot add unrelated diffs.
        selected = semantics if name in involved else result["adapters"][result["baseline"]]["semantics"]
        adapters[name] = {"inline": {"semantics": selected}}
    return {
        "name": f"{result['name']}-minimal-repro",
        "baseline": result["baseline"],
        "adapters": adapters,
        "compare": compare,
    }


def compact(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def render_html(result: dict[str, Any]) -> str:
    if not isinstance(result, dict) or not isinstance(result.get("diffs"), list):
        raise WireDiffError("result JSON must contain diffs[]")
    rows = []
    for item in result["diffs"]:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(item['category']))}</td>"
            f"<td>{html.escape(str(item['probe']))}</td>"
            f"<td>{html.escape(str(item['baselineAdapter']))}</td>"
            f"<td><code>{html.escape(compact(item['baselineValue']))}</code></td>"
            f"<td>{html.escape(str(item['adapter']))}</td>"
            f"<td><code>{html.escape(compact(item['value']))}</code></td>"
            "</tr>"
        )
    if not rows:
        rows.append('<tr><td colspan="6">No semantic divergences.</td></tr>')
    summary = result.get("summary", {})
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'"><title>{html.escape(str(result.get('name', 'SDK WireDiff')))}</title><style>
:root{{font-family:ui-sans-serif,system-ui,sans-serif;color:#172033;background:#f4f7fb}}body{{max-width:1200px;margin:auto;padding:2rem}}.summary{{display:flex;gap:1rem;flex-wrap:wrap}}.metric{{background:#fff;border:1px solid #d7dfeb;border-radius:10px;padding:1rem;min-width:11rem}}table{{width:100%;border-collapse:collapse;background:#fff;margin-top:1.5rem}}th,td{{border:1px solid #d7dfeb;padding:.7rem;text-align:left;vertical-align:top}}th{{background:#172033;color:#fff}}code{{white-space:pre-wrap;overflow-wrap:anywhere}}footer{{margin-top:2rem;color:#566070}}</style></head><body>
<header><h1>{html.escape(str(result.get('name', 'SDK WireDiff')))}</h1><p>Semantic cross-SDK differential report.</p></header>
<section class="summary"><div class="metric"><strong>{summary.get('adapterCount', 0)}</strong><br>adapters</div><div class="metric"><strong>{summary.get('divergenceCount', 0)}</strong><br>divergences</div><div class="metric"><strong>{html.escape(', '.join(summary.get('divergentCategories', [])) or 'none')}</strong><br>categories</div></section>
<table><thead><tr><th>Category</th><th>Probe</th><th>Baseline</th><th>Baseline value</th><th>Adapter</th><th>Observed value</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<footer>Static report generated by SDK WireDiff. No remote assets, scripts, or traffic captures.</footer></body></html>\n"""


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Compare synthetic/captured TypeScript, Python, and Go SDK observations")
    subparsers = root.add_subparsers(dest="command", required=True)
    compare = subparsers.add_parser("compare", help="run one fixture manifest")
    compare.add_argument("manifest", type=Path)
    compare.add_argument("--json", type=Path, default=Path("wirediff.json"))
    compare.add_argument("--html", type=Path, default=Path("wirediff.html"))
    compare.add_argument("--repro", type=Path, default=Path("wirediff.repro.json"))
    compare.add_argument("--allow-command", action="store_true", help="run trusted adapter argv from the manifest")
    render = subparsers.add_parser("render", help="render an existing result JSON")
    render.add_argument("result", type=Path)
    render.add_argument("--output", type=Path, required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "compare":
        result = compare_manifest(args.manifest, allow_command=args.allow_command)
        write_text(args.json, canonical_json(result))
        write_text(args.html, render_html(result))
        write_text(args.repro, canonical_json(minimal_repro(result)))
        return 0
    result = read_json(args.result)
    write_text(args.output, render_html(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except WireDiffError as error:
        print(f"sdk-wirediff: {error}", file=sys.stderr)
        raise SystemExit(1) from None
