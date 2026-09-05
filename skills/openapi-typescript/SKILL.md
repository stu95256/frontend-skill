---
name: openapi-typescript
description: Generate and maintain deterministic TypeScript types from OpenAPI 3.x schemas with the openapi-typescript CLI. Use when an API schema changes, generated API types drift, or a project needs reproducible schema-to-TypeScript generation.
license: MIT; see LICENSE
metadata:
  catalog-origin: project-curated
  tool-source: https://github.com/openapi-ts/openapi-typescript
  tool-source-commit: 0cc7ee77d28359c7901d9cd3b5733b70a050ea49
  source-docs: docs/cli.md, docs/advanced.md
  tested-cli-version: "7.13.0"
---

# OpenAPI TypeScript Generation

Use a reproducible CLI pipeline. Do not manually transcribe an OpenAPI schema into interfaces and do not invent runtime type guards from static types.

## Workflow

1. Locate the canonical OpenAPI JSON/YAML file or URL and inspect the project's package manager and existing scripts.
2. Prefer the project's pinned `openapi-typescript` dependency and existing generation script. Add a dev dependency only when the project has no generator.
3. Generate into a clearly marked generated file:

```bash
# npm
npx openapi-typescript ./openapi.yaml -o ./src/api/schema.d.ts

# pnpm
pnpm exec openapi-typescript ./openapi.yaml -o ./src/api/schema.d.ts

# bun
bunx openapi-typescript ./openapi.yaml -o ./src/api/schema.d.ts
```

4. Add or reuse a package script so CI and contributors run the same command:

```json
{
  "scripts": {
    "api:types": "openapi-typescript ./openapi.yaml -o ./src/api/schema.d.ts"
  }
}
```

5. Run the script twice and require a clean second diff. A non-idempotent output indicates an unstable input or pipeline.
6. Run the project's type checker and tests that consume the generated declarations.
7. Commit the schema and generated output together when the repository tracks generated files.

## Rules

- Treat the OpenAPI document as the source of truth; fix schema defects upstream rather than patching generated declarations.
- Preserve `operationId`, required/optional properties, nullable semantics, enums, formats, and component references from the schema.
- Never edit the generated `.d.ts` by hand.
- Pin the generator through the project lockfile; do not rely on an unpinned global install.
- Do not put API credentials in schema URLs, scripts, logs, or generated files.
- Remote schemas require an explicit network/reproducibility decision. Prefer a checked-in schema snapshot or a separately verified fetch step.
- Static TypeScript declarations do not validate runtime data. If runtime validation is required, choose a schema-driven validator or generated runtime client as a separate, explicit step.

## Verification Checklist

- [] The input is the canonical OpenAPI 3.x schema.
- [] The command uses the project's package manager and locked dependency.
- [] The generated file carries no manual edits.
- [] A second generation run produces no diff.
- [] Type checking and relevant tests pass.
- [] No secrets or authenticated schema URL leaked into tracked files.

## References

- https://openapi-ts.dev/openapi-typescript/
- https://github.com/openapi-ts/openapi-typescript
