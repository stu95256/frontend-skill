# Security Review Checklist

- Identify trust boundaries, untrusted inputs, authorization decisions, and sensitive outputs.
- Reject XSS, injection, path traversal, unsafe deserialization, SSRF, and open redirects with concrete evidence.
- Check authentication and authorization separately; enforce access at the server or authoritative boundary.
- Keep secrets out of client bundles, logs, errors, fixtures, and committed files.
- Review dependencies, lifecycle scripts, integrity controls, and lockfile changes.
- Report path, line, exploit or misuse path, impact, confidence, and the smallest safe correction.
