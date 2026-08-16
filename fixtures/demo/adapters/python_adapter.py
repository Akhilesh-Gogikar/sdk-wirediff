#!/usr/bin/env python3
"""Synthetic command-produced Python SDK observation; performs no I/O."""

import json


print(json.dumps({
    "request": {
        "method": "GET",
        "url": "https://synthetic.invalid/widgets?page_size=20&include_archived=false",
        "headers": {"Accept": "application/json"},
    },
    "attempts": [{"status": 429}, {"status": 429}, {"status": 200}],
    "error": {"code": "rate_limited", "status": 429},
    "response": {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "items": [{"id": "widget-1", "label": "Alpha"}],
            "meta": {},
            "next_cursor": "cursor-2",
            "has_more": True,
        },
    },
}, sort_keys=True))
