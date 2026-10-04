# Accessibility baseline

SDK WireDiff’s CLI is plain-text and its generated semantic report is static HTML with no scripts or remote assets.

## Implemented baseline

- Semantic `header`, `main`, summary section, table, and `footer` landmarks.
- A keyboard-visible skip link and focus outline around the horizontally scrollable table region.
- A descriptive table caption, column-header `scope`, region label, and baseline/adapter names in every difference row.
- Text counts and category labels so color is never the only signal.
- High-contrast text, borders, headers, and focus indicators; responsive horizontal table access at narrow widths.
- Escaped observation content and a restrictive content security policy.

## Release checks

Before release, traverse with only Tab/Shift+Tab, zoom to 200%, inspect narrow width, confirm visible focus, and read landmarks/caption/headers with a screen reader. Test both the three-difference fixture and a zero-difference result. Verify cell reading order remains understandable without color.

## Known limits

Large JSON values can be verbose for screen readers, and the report does not provide interactive column filtering or a condensed accessible view. Automated accessibility conformance and multiple screen-reader/browser combinations are not yet in CI. CLI diagnostics do not have terminal-specific accessibility modes.

Report defects with the bug template and prefix the title `accessibility:`. Use synthetic or redacted observations. Security-sensitive findings belong in the [private advisory form](https://github.com/Akhilesh-Gogikar/sdk-wirediff/security/advisories/new).
