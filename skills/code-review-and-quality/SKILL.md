---
name: code-review-and-quality
description: Review a code change or pull request for concrete, evidence-backed regressions across correctness, maintainability, security and performance. Use for requested reviews or pre-merge assessment, including pasted diffs.
---

# Code Review and Quality

## Overview

Review covers five axes: correctness, readability, architecture, security, and performance. Checklists identify investigation candidates, not automatic findings. Review only the assigned scope and stay read-only.

**The approval standard:** Approve a change when it definitely improves overall code health, even if it isn't perfect. Perfect code doesn't exist — the goal is continuous improvement. Don't block a change because it isn't exactly how you would have written it. If it improves the codebase and follows the project's conventions, approve it.

## Finding threshold

Report only discrete, actionable defects introduced or worsened by the change with meaningful impact. Establish expected behavior from an applicable requirement, caller, test, API contract or documented project rule; trace a reachable trigger to an actual wrong outcome and compare before/after behavior. Conditional defects count when their preconditions are supported. Maintainability findings need a concrete ownership/dependency consequence or an applicable documented rule, not a preferred abstraction.

Before retaining a candidate, try to disprove it using surrounding callers, upstream validation, guards, intentional behavior and the actual dependency/config versions. Syntax, file size, a checklist item, reviewer agreement or confidence alone is not proof. Static evidence can establish a defect without execution. Do not invent requirements, numerical performance claims or rigor absent from the project. Pre-existing issues, missing tests alone and optional simplifications are not defect findings. Return no findings when none meet this threshold; missing essential context is an evidence limit, not a bug or approval.

The coordinator's scope, finding gate, output schema and verification permissions govern this Skill. In the three Frontend Review workflows, follow the [shared contract](../frontend-staged-review-workflow/references/review-contract.md), including candidate evidence fields and validator checks; do not import those workflows' quorum/schema into single-task reviews. Read-only review never authorizes edits, mutation testing, installation or checks that write into the reviewed checkout. The [precision references](../frontend-staged-review-workflow/references/review-precision.md) explain the policy and behavioral evaluation approach.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)

## The Five-Axis Review

Every review evaluates code across these dimensions:

### 1. Correctness

Does the code do what it claims to do?

- Does it match the spec or task requirements?
- Are edge cases handled (null, empty, boundary values)?
- Are error paths handled (not just the happy path)?
- Does it pass all tests? Are the tests actually testing the right things?
- Are there off-by-one errors, race conditions, or state inconsistencies?

### 2. Readability & Simplicity

Can another engineer (or agent) understand this code without the author explaining it?

- Are names descriptive and consistent with project conventions? (No `temp`, `data`, `result` without context)
- Is the control flow straightforward (avoid nested ternaries, deep callbacks)?
- Is the code organized logically (related code grouped, clear module boundaries)?
- Are there any "clever" tricks that should be simplified?
- Does complexity obscure an invariant or create a specific maintenance failure? Fewer lines alone is not evidence of improvement.
- Do abstractions preserve actual domain and ownership contracts? A different abstraction is not automatically better.
- Would comments help clarify non-obvious intent? (But don't comment obvious code.)
- Are there dead code artifacts: no-op variables (`_unused`), backwards-compat shims, or `// removed` comments?
- Does a new conditional violate a specific invariant or ownership boundary? Show that consequence before proposing extraction.
- Do repeated conditionals actually diverge or break a contract? Repetition alone does not establish a missing model or dispatcher.

### 3. Architecture

Does the change fit the system's design?

- Does it follow existing patterns or introduce a new one? If new, is it justified?
- Does it maintain clean module boundaries?
- Is there code duplication that should be shared?
- Are dependencies flowing in the right direction (no circular dependencies)?
- Is the abstraction level appropriate (not over-engineered, not too coupled)?
- Does the refactor introduce a concrete regression in dependencies, ownership or behavior? Relocating logic without reducing line count or concepts is not itself a defect.
- Does feature-specific logic violate the shared module's documented responsibility or affect a demonstrated consumer? Check the actual boundary and existing helpers before suggesting a move.
- **Are type boundaries explicit?** Question gratuitous `any`/`unknown`/optional/casts and silent fallbacks that paper over an unclear invariant — making the boundary explicit often makes the surrounding control flow simpler.

### 4. Security

For detailed security guidance, see `security-and-hardening`. Does the change introduce vulnerabilities?

- Is user input validated and sanitized?
- Are secrets kept out of code, logs, and version control?
- Is authentication/authorization checked where needed?
- Are SQL queries parameterized (no string concatenation)?
- Are outputs encoded to prevent XSS?
- Are dependencies from trusted sources with no known vulnerabilities?
- Is data from external sources (APIs, logs, user content, config files) treated as untrusted?
- Are external data flows validated at system boundaries before use in logic or rendering?

### 5. Performance

For detailed profiling and optimization, see `performance-optimization`. Does the change introduce performance problems?

- Any N+1 query patterns?
- Any unbounded loops or unconstrained data fetching?
- Any synchronous operations that should be async?
- Any unnecessary re-renders in UI components?
- Any missing pagination on list endpoints?
- Any large objects created in hot paths?

## Structural Remedies

When you flag a structural problem, propose the move — not just the problem. A review that only says "this is complex" leaves the author guessing. Reach for a named restructuring:

- **Replace a chain of conditionals** with a typed model or an explicit dispatcher.
- **Collapse duplicate branches** into a single clearer flow.
- **Separate orchestration from business logic** so each reads on its own.
- **Move feature-specific logic** out of a shared module into the package that owns the concept.
- **Reuse the canonical helper** instead of a bespoke near-duplicate.
- **Make a type boundary explicit** so downstream branching disappears.
- **Delete a pass-through wrapper** that adds indirection without clarifying the API.
- **Extract a helper, or split a large file** into focused modules.

Prefer the remedy that removes moving pieces over one that spreads the same complexity around.

## Change Sizing

Small, focused changes are easier to review. These are planning heuristics, not finding or blocking thresholds:

```
~100 lines changed   → Good. Reviewable in one sitting.
~300 lines changed   → Acceptable if it's a single logical change.
~1000 lines changed  → May require more review chunks or context.
```

**Watch file size, not just diff size.** A large file can warrant closer inspection, but size alone does not demonstrate a defect or require decomposition. Trace actual coupling, ownership and changed behavior.

**What counts as "one change":** A single self-contained modification that addresses one thing, includes related tests, and keeps the system functional after submission. One part of a feature — not the whole feature.

**Splitting strategies when a change is too large:**

| Strategy | How | When |
|----------|-----|------|
| **Stack** | Submit a small change, start the next one based on it | Sequential dependencies |
| **By file group** | Separate changes for groups needing different reviewers | Cross-cutting concerns |
| **Horizontal** | Create shared code/stubs first, then consumers | Layered architecture |
| **Vertical** | Break into smaller full-stack slices of the feature | Feature work |

**When large changes are acceptable:** Complete file deletions and automated refactoring where the reviewer only needs to verify intent, not every line.

Separate refactoring from feature work when that helps review or follows project policy. A mixed diff is not automatically a defect; report actual coverage limits instead of requiring a split merely by category.

## Change Descriptions

Every change needs a description that stands alone in version control history.

**First line:** Short, imperative, standalone. "Delete the FizzBuzz RPC" not "Deleting the FizzBuzz RPC." Must be informative enough that someone searching history can understand the change without reading the diff.

**Body:** What is changing and why. Include context, decisions, and reasoning not visible in the code itself. Link to bug numbers, benchmark results, or design docs where relevant. Acknowledge approach shortcomings when they exist.

**Anti-patterns:** "Fix bug," "Fix build," "Add patch," "Moving code from A to B," "Phase 1," "Add convenience functions."

## Review Process

### Step 1: Understand the Context

Before looking at code, understand the intent:

```
- What is this change trying to accomplish?
- What spec or task does it implement?
- What is the expected behavior change?
```

### Step 2: Review the Tests First

Tests reveal intent and coverage:

```
- Do tests exist for the change?
- Do they test behavior (not implementation details)?
- Are edge cases covered?
- Do tests have descriptive names?
- Would the tests catch a regression if the code changed?
```

Use existing tests as evidence of intent, then inspect whether their assertions match the applicable contract. Do not edit code or run mutation testing during review. Missing tests or an undetected hypothetical mutation alone do not establish a product defect. Changed assertions or mocks can be findings when they demonstrably conceal an actual behavior error. Report unobserved checks as limits rather than claiming they passed or failed.

### Step 3: Review the Implementation

Walk through the code with the five axes in mind:

```
For each file changed:
1. Correctness: Does this code do what the test says it should?
2. Readability: Can I understand this without help?
3. Architecture: Does this fit the system?
4. Security: Any vulnerabilities?
5. Performance: Any bottlenecks?
```

### Step 4: Categorize Findings

Use the coordinator's severity/schema when supplied. Otherwise label confirmed defects by demonstrated impact. The following labels may separate optional feedback only when the user explicitly requested broader critique; do not populate optional/nit sections in a defects-only review:

| Prefix | Meaning | Author Action |
|--------|---------|---------------|
| *(no prefix)* | Required change | Must address before merge |
| **Critical:** | Blocks merge | Security vulnerability, data loss, broken functionality |
| **Nit:** | Minor, optional | Author may ignore — formatting, style preferences |
| **Optional:** / **Consider:** | Suggestion | Worth considering but not required |
| **FYI** | Informational only | No action needed — context for future reference |

This prevents authors from treating all feedback as mandatory and wasting time on optional suggestions.

**Lead with what matters.** Order confirmed findings by impact: correctness and security first, then demonstrated structural/performance regressions. Omit cosmetic nits and unsupported simplifications. A short accurate review is preferable to filling every category.

### Step 5: Verify the Verification

Check the author's verification story:

```
- What tests were run?
- Did the build pass?
- Was the change tested manually?
- Are there screenshots for UI changes?
- Is there a before/after comparison?
```

## Multi-Model Review Pattern

When the coordinator calls for independent reviews, different models may provide different perspectives:

```
Model A writes the code
    │
    ▼
Model B reviews for correctness and architecture
    │
    ▼
Model A addresses the feedback
    │
    ▼
Human makes the final call
```

Different models may have different blind spots, but agreement is not proof. Respect the coordinator's delegation limits; independently validate claims before publication rather than adding reviewers to resolve an unsupported assertion.

**Example prompt for a review agent:**
```
Review this code change for correctness, security, and adherence to
our project conventions. The spec says [X]. The change should [Y].
Report only introduced defects supported by the applicable contract,
reachable scenario, before/after evidence and checked protections.
Return no findings if none qualify; disclose missing essential context.
```

## Dead Code Hygiene

After any refactoring or implementation change, check for orphaned code:

1. Search real consumers, exports, dynamic registration and compatibility contracts before declaring something unused.
2. Report only introduced dead code that meets the finding threshold; absence of a text reference alone does not prove that a public or dynamically used symbol is dead.
3. Keep review read-only. Return a supported correction to the coordinator; do not ask to delete code or begin cleanup during review.

## Review Speed

Slow reviews block entire teams. The cost of context-switching to review is less than the waiting cost imposed on others.

- **Respond within one business day** — this is the maximum, not the target
- **Ideal cadence:** Respond shortly after a review request arrives, unless deep in focused coding. A typical change should complete multiple review rounds in a single day
- **Prioritize fast individual responses** over quick final approval. Quick feedback reduces frustration even if multiple rounds are needed
- **Large changes:** Review in complete chunks under the assigned coverage plan; disclose any scope that could not be inspected.

## Handling Disagreements

When resolving review disputes, apply this hierarchy:

1. **Technical facts and data** override opinions and preferences
2. **Style guides** are the absolute authority on style matters
3. **Software design** must be evaluated on engineering principles, not personal preference
4. **Codebase consistency** is acceptable if it doesn't degrade overall health

Distinguish a confirmed introduced defect from pre-existing cleanup or a preferred design. Keep supported defects visible; do not expand the review into surrounding refactors or require unrelated issue filing.

## Honesty in Review

When reviewing code — whether written by you, another agent, or a human:

- **Don't rubber-stamp.** "LGTM" without evidence of review helps no one.
- **Don't soften real issues.** "This might be a minor concern" when it's a bug that will hit production is dishonest.
- **Quantify only with evidence.** Cite measurements or a demonstrable bound on repeated work; do not invent latency, traffic or data-volume assumptions.
- **Push back on approaches with clear problems.** Sycophancy is a failure mode in reviews. If the implementation has issues, say so directly and propose alternatives.
- **Accept override gracefully.** If the author has full context and disagrees, defer to their judgment. Comment on code, not people — reframe personal critiques to focus on the code itself.

## Dependency Discipline

Part of code review is dependency review:

**Before adding any dependency:**
1. Does the existing stack solve this? (Often it does.)
2. How large is the dependency? (Check bundle impact.)
3. Is it actively maintained? (Check last commit, open issues.)
4. Does it have known vulnerabilities? (`npm audit`)
5. What's the license? (Must be compatible with the project.)

**Rule:** Prefer standard library and existing utilities over new dependencies. Every dependency is a liability.

**Upgrading an existing dependency** is a code change like any other, and the riskiest upgrades are the ones merged in bulk with a message like "bump deps." Review them with the same discipline:

1. **Read the changelog, not just the version number.** Semver is a promise the maintainer may not have kept — a "patch" can carry a behavioral change. For a major bump, read the migration notes and find what breaks.
2. **One dependency per change.** Upgrade and merge them individually (or in small related groups). When a bulk bump breaks the build, you've lost which package did it; a single-package change makes the cause obvious and the revert clean.
3. **Check compatibility evidence.** Compare pinned versions, relevant APIs, changelogs and observed check results. Thin coverage is an evidence limit, not by itself a regression. Passing tests do not disprove a reachable compatibility defect established from source.
4. **Mind the transitive graph.** Most installed packages are ones nobody chose directly. Review the lockfile diff, not just `package.json`; a single direct bump can pull in dozens of indirect changes.
5. **Keep the lockfile honest.** Commit it, review its diff, and never hand-edit it. The lockfile is the thing that actually pins what ships.

For triaging `npm audit` findings and supply-chain risk (typosquatting, compromised maintainers), follow the `security-and-hardening` skill — this section covers the upgrade *workflow*, that one covers the security verdict.

## The Review Checklist

```markdown
## Review: [PR/Change title]

### Context
- [ ] I understand what this change does and why

### Correctness
- [ ] Change matches spec/task requirements
- [ ] Edge cases handled
- [ ] Error paths handled
- [ ] Tests cover the change adequately

### Readability
- [ ] Names are clear and consistent
- [ ] Logic is straightforward
- [ ] No unnecessary complexity

### Architecture
- [ ] Follows existing patterns
- [ ] No unnecessary coupling or dependencies
- [ ] Appropriate abstraction level
- [ ] Refactors reduce complexity rather than relocate it
- [ ] No feature logic in shared modules; file stays within a healthy size

### Security
- [ ] No secrets in code
- [ ] Input validated at boundaries
- [ ] No injection vulnerabilities
- [ ] Auth checks in place
- [ ] External data sources treated as untrusted

### Performance
- [ ] No N+1 patterns
- [ ] No unbounded operations
- [ ] Pagination on list endpoints

### Verification
- [ ] Tests pass
- [ ] Build succeeds
- [ ] Manual verification done (if applicable)

### Verdict
- [ ] **Approve** — Ready to merge
- [ ] **Request changes** — Issues must be addressed
```
## See Also

- For detailed security review guidance, see [security checklist](references/security-checklist.md).
- For performance review checks, see [performance checklist](references/performance-checklist.md).

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It works, that's good enough" | Working code that's unreadable, insecure, or architecturally wrong creates debt that compounds. |
| "I wrote it, so I know it's correct" | Authors are blind to their own assumptions. Every change benefits from another set of eyes. |
| "We'll clean it up later" | Keep confirmed introduced defects visible; distinguish them from unrelated cleanup and optional redesign. |
| "AI-generated code is probably fine" | AI code needs more scrutiny, not less. It's confident and plausible, even when wrong. |
| "The tests pass, so it's good" | Tests are necessary but not sufficient. They don't catch architecture problems, security issues, or readability concerns. |
| "The refactor makes it cleaner" | Check actual contracts, behavior and dependencies rather than accepting or rejecting an aesthetic claim. |
| "It's only a small addition to this file" | Inspect the resulting behavior; neither small diff size nor a large file proves correctness or a defect. |
| "It's just a version bump" | A bump is a behavior change you didn't write. Read the changelog; semver doesn't guarantee no breakage. |
| "I'll upgrade everything in one PR to save time" | A bulk bump that breaks the build hides which package did it. One dependency per change keeps the cause and the revert clean. |

## Red Flags

- PRs merged without any review
- Review that only checks if tests pass (ignoring other axes)
- "LGTM" without evidence of actual review
- Security-sensitive changes without security-focused review
- A declared review scope with uninspected chunks or missing essential context
- Changed tests that conceal a demonstrated behavior error
- Review comments without severity labels — makes it unclear what's required vs optional
- Dismissing a confirmed introduced defect without addressing its evidence
- A refactor that introduces a concrete ownership, dependency or behavior regression
- A new conditional or helper that demonstrably violates an existing contract
- A bulk "bump dependencies" PR with no changelog review and no per-package isolation
- A lockfile change that's hand-edited, uncommitted, or merged without reviewing its diff

## Verification

After review is complete, report which of these were actually observed. Unexecuted checks and missing evidence are limits, not automatic findings or claims of success:

- [ ] All Critical issues are resolved
- [ ] All Required (no-prefix) changes are resolved or explicitly deferred with justification
- [ ] Tests pass
- [ ] Build succeeds
- [ ] The verification story is documented (what changed, how it was verified)
- [ ] Dependency upgrades were reviewed against their changelog, isolated per package, and verified by a green suite with the lockfile diff reviewed

**Structural findings:** require a specific introduced contract violation or meaningful dependency/ownership consequence, with before/after evidence and checked counterevidence. File size, repeated branches, a near-duplicate helper or a silent fallback are investigation signals, not presumptive blockers. Propose restructuring only after establishing the defect.
