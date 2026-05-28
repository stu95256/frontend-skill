# TypeScript Code Reviewer Research Sources

調查日期：2026-05-28

## 結論

本專案原本已有：

- `code-review-excellence`：通用 code review skill，含 `reference/typescript.md`。
- `code-review-and-quality` / `requesting-code-review`：通用 review / pre-commit workflow。
- `typescript-advanced-types`：TypeScript advanced type skill。

但沒有一個 flat `skills/<name>/SKILL.md` 是「專門用來 reviewer TypeScript / TSX code」的 top-level skill。因此新增 `skills/typescript-code-reviewer/`。

網路上有找到真正叫 `typescript-code-review` 的 SKILL.md，但主要原始 repo 沒有明確 LICENSE，因此沒有直接複製內容；本 skill 改用官方文件與 MIT/Apache-2.0 來源整理成新的專案 skill。

## Dedicated TypeScript reviewer skill candidates

| Source | URL | Evidence | License / caveat | Decision |
|---|---|---|---|---|
| Exploration-labs/typescript-code-review | https://github.com/Exploration-labs/typescript-code-review/blob/main/SKILL.md | `name: typescript-code-review`; description states comprehensive TypeScript code reviews covering type safety, performance, security, code quality. Commit `3cbb6e8c0e21d3a33f892a4b49c63dcbc121e061`. | No LICENSE file found. | Recorded only; not copied verbatim. |
| jdevera/agent-skills `skills/typescript-code-review` | https://github.com/jdevera/agent-skills/blob/main/skills/typescript-code-review/SKILL.md | Same/similar dedicated TypeScript code review skill, with references/checklists. Commit `6528c9889d468fcd121f58fda4b6e073d9313c1c`. | No LICENSE file found. | Recorded only; not copied verbatim. |
| NeverSight/learn-skills.dev mirror | https://github.com/NeverSight/learn-skills.dev/tree/main/data/skills-md/exploration-labs/typescript-code-review/typescript-code-review | Mirror of Exploration-labs skill. Commit `04de12423304d4c87374cd85afb4570576a2616b`. | Mirror, not upstream source; license unclear. | Recorded only. |

## License-clear code review skill sources

| Source | URL | License | What was useful |
|---|---|---|---|
| awesome-skills/code-review-skill | https://github.com/awesome-skills/code-review-skill | MIT | Existing `code-review-excellence` skill and `reference/typescript.md`; broad PR review framing plus TypeScript checklist ideas. Commit `aca7203b420bdf9664c25c3adbb426bec164c233`. |
| William-Yeh/common-code-reviewer | https://github.com/William-Yeh/common-code-reviewer | Apache-2.0 | Principal-engineer review persona, severity/output discipline, and JS/TS review rules in `skill/references/typescript.md`. Commit `96c43a797788444f362aae21c7ace7ae39e6ee68`. |
| yoriiis/ai-skills `frontend-code-review` | https://github.com/yoriiis/ai-skills/tree/main/skills/frontend-code-review | MIT | Frontend MR/PR review workflow, XSS/a11y/performance framing, JS/TS reference. Commit `6952aa721f98ba7a478485cf6435a1f39ab2bb57`. |
| scottgl9/skelm-code-reviewer | https://github.com/scottgl9/skelm-code-reviewer | MIT | PR reviewer agent + language-specific review skill; JS/TS reference includes unsafe `any`, `as unknown as T`, type-only imports, discriminated unions. Commit `b474dd2f7e10a570ab081e666e5b06cf1034bfc8`. |
| alexei-led/cc-thingz `reviewing-code` | https://github.com/alexei-led/cc-thingz/tree/master/dist/claude/plugins/dev-flow/skills/reviewing-code | MIT | TypeScript 5.x review slice with tooling-first mindset and manual focus areas. Commit `ad9b8c1707d89185175153183714c4670249a037`. |
| leejpsd/typescript-react-patterns | https://github.com/leejpsd/typescript-react-patterns | MIT | TypeScript + React review risk rules: `any`, `as` on external data, non-null assertions, runtime validation, hook pitfalls. Commit `ec6baf986dfe8e02c1ef4c978124c0ce3a3f762f`. |

## Official / authoritative references used

| Area | Sources | Review rules extracted |
|---|---|---|
| TypeScript config and narrowing | https://www.typescriptlang.org/tsconfig/ ; https://www.typescriptlang.org/docs/handbook/2/narrowing.html ; https://github.com/microsoft/TypeScript/wiki/Performance | Prefer `strict`, `noImplicitAny`, `strictNullChecks`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `useUnknownInCatchVariables`; use narrowing/discriminated unions; watch type complexity. |
| typescript-eslint typed linting | https://typescript-eslint.io/getting-started/typed-linting/ ; rules such as `no-explicit-any`, `no-unsafe-assignment`, `no-floating-promises`, `no-misused-promises`, `switch-exhaustiveness-check` | Use typed linting to catch unsafe type escapes and Promise mistakes. |
| ESLint core correctness/security rules | https://eslint.org/docs/latest/rules/no-eval ; `no-implied-eval`, `no-new-func`, `no-async-promise-executor`, `require-atomic-updates`, `no-await-in-loop` | Flag dynamic code execution, async executor bugs, race-prone updates, unnecessary serial awaits. |
| React + TypeScript / Hooks | https://react.dev/learn/typescript ; https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks ; https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps ; https://react.dev/reference/rules/components-and-hooks-must-be-pure | Review props/state/context typing, hook placement, dependency arrays, purity, memoization. |
| OWASP / frontend security | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html ; https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html ; https://owasp.org/www-project-code-review-guide/ ; https://web.dev/articles/strict-csp | Treat untrusted data as hostile; inspect dangerous DOM sinks, unsafe URLs, sanitization, CSP/Trusted Types defense-in-depth. |
| Style/testing | https://google.github.io/styleguide/tsguide.html ; https://testing-library.com/docs/guiding-principles/ | Assertions do not add runtime checks; tests should resemble user behavior and cover error/security paths. |

## Search queries used / reusable

```text
filename:SKILL.md "typescript-code-review"
filename:SKILL.md "TypeScript" "code review"
"typescript-code-review" "SKILL.md"
"TypeScript / JavaScript Review Rules" "SKILL.md"
"frontend-code-review" "JavaScript / TypeScript"
"TypeScript Review Slice" "SKILL.md"
"TypeScript" "PR reviewer" "SKILL.md"
```

GitHub code search API may require authentication; fallback methods used here were raw GitHub URLs, `git ls-remote`, repository pages, and direct file fetches.
