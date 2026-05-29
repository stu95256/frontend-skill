# TypeScript Reviewer Checklist

Use this shorter checklist when the full `SKILL.md` is too large for a review prompt.

## Blocker/Major checks

- `tsc --noEmit` or project typecheck passes, or failures are documented as pre-existing.
- `strict` config and nullability assumptions are understood.
- No new unbounded `any`; unknown external data is validated/narrowed.
- No unsafe `as`, `as unknown as T`, or non-null `!` at trust boundaries.
- Route params, query strings, localStorage, FormData, and JSON parse results are validated before use.
- Promises are awaited/returned/caught or intentionally `void`ed; no async Promise executors.
- Catch variables are narrowed from `unknown`; thrown values are `Error`-like.
- React hooks obey Rules of Hooks; dependencies are complete; effects clean up subscriptions/timers/listeners.
- No unsafe DOM sinks (`innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`) without sanitizer and justification.
- URLs are scheme-validated before rendering links/redirects.
- Tests cover success, empty/null/malformed data, async error, and security-sensitive paths.

## Output format

```markdown
TypeScript Review Verdict: PASS | CHANGES_REQUESTED

Summary:
- ...

Findings:
1. [Blocker|Major|Minor|Nit] file:line — issue
   Why it matters: ...
   Suggested fix: ...

Verification:
- typecheck: ...
- lint: ...
- tests: ...
```
