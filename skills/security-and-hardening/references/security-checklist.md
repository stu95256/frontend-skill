# Security and Supply-Chain Checklist

- Map trust boundaries, identities, authorization checks, sensitive data, and external calls.
- Validate input at authoritative boundaries and encode output for its exact sink.
- Use parameterized queries and safe APIs; reject dynamic code execution and unsafe deserialization.
- Protect secrets, session tokens, logs, caches, browser storage, and cross-tenant data.
- Resolve the owning package manager from `packageManager`, lockfile, and CI; stop if they disagree.
- Install frozen/immutable with lifecycle scripts disabled until reviewed; approve only necessary scripts.
- Review dependency source, exact version, integrity, advisories, and transitive changes.
- Verify with the project's security checks and record residual risk.
