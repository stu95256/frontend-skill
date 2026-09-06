---
description: Frontend implementation standards for JavaScript, TypeScript, React, styles, and tests.
applyTo: "**/*.{js,jsx,mjs,cjs,ts,tsx,css,scss,less,html,json}"
---

# Frontend Engineering

- Inspect package manifests, framework versions, configuration, definitions, usages, and nearby working patterns before editing.
- Preserve existing architecture and naming. Use descriptive domain names and keep meaningful qualifiers; do not shorten identifiers until they become ambiguous.
- Make the smallest complete change and avoid unrelated refactors or formatting churn.
- Treat accessibility, loading, empty, error, responsive, localization, and keyboard states as part of feature correctness when applicable.
- Do not hide type or runtime problems with `any`, unsafe assertions, blanket lint disables, empty catches, or arbitrary delays.
- Verify behavior with the project's real scripts and observable runtime evidence. Report exact commands, results, skipped checks, and remaining risks.
