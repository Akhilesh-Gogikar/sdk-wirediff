# Security policy

## Supported versions

| Version | Security fixes |
|---|---|
| 0.1.x | Supported while it is the current line |
| Earlier prototypes | Not supported |

## Report privately

Use a [private GitHub security advisory](https://github.com/akigogikar/sdk-wirediff/security/advisories/new). Do not open a public issue for command-execution problems, path traversal, unsafe parsing, redaction bypass, report injection, secret exposure, or dependency-chain vulnerabilities.

Include the affected version or commit, impact, a minimal synthetic reproduction, and suggested mitigation. Never send real credentials or production traffic. You should receive an acknowledgement when practical; remediation timing depends on severity and maintainer availability. Please allow coordinated remediation before disclosure.

## Security model

SDK WireDiff treats manifests and observations as untrusted data, but an explicitly enabled adapter command is trusted executable code with the invoking user’s host permissions. The tool is not a sandbox, traffic recorder, credential broker, or safe way to execute an untrusted fixture. Common credential headers and secret-like query fields are redacted, but arbitrary bodies can still contain sensitive values. See [PRIVACY.md](docs/PRIVACY.md).
