---
name: test-driven-development
description: Build or fix behavior test-first with focused red-green-refactor cycles. Use when the user requests TDD or a behavior change needs a reproducible regression test.
license: MIT; see LICENSE
metadata:
  source: https://github.com/mattpocock/skills
  source-commit: 59db609eb1e18aaf59b63284d0e52255aff0c63c
  source-path: skills/engineering/tdd
  adaptation: VS Code workflow; authorized test boundaries; proportional verification
---

# Test-Driven Development

Prove behavior through a public interface. Observe the intended failure, implement the smallest change, then refactor while green. Tests should survive changes to internal structure.

## Choose the behavior and boundary

Inspect the requirement, implementation, relevant tests and repository commands. Use established domain terms from a glossary or ADR when relevant.

Name the observable behavior and the interface exposing it: a function result, rendered DOM, route response or persisted state retrieved through a public API. State which failure the test catches.

Reuse boundaries authorized by the task or plan. Ask only when an unresolved product decision or a new external side effect makes the boundary unclear. Routine test design does not require another approval.

Choose the smallest reliable test level. Do not manufacture tests for prose, trivial forwarding, generated output or a reversible cosmetic change without a meaningful failure to catch.

## One vertical slice at a time

1. **Red:** write one test with an independently derived expected value. Confirm it fails because behavior is missing or wrong, rather than because imports or setup are broken.
2. **Green:** make the smallest implementation change and run the focused test.
3. **Refactor:** improve demonstrated duplication or design problems while keeping behavior green. Avoid speculative abstractions.
4. Repeat for the next required behavior. Do not write every imagined test before learning from the first implementation.

Preserve existing code and user work. Establish a regression or characterization test; do not delete working code merely because it predates its tests.

## Tests worth keeping

Read [tests.md](tests.md) for assertion design and [mocking.md](mocking.md) when a dependency needs a double.

- Derive expectations from the specification, a worked example or a known literal, never from the implementation's own helper.
- Observe caller-visible results rather than private methods, incidental call order or a mocked component's existence.
- Keep behavior under test real. A boundary call's payload or ordering can be asserted when it is itself the contract.
- Cover meaningful pending, failure, empty and boundary outcomes.
- Avoid blanket coverage targets or a test for every function. Name the behavior error each test detects.

## Verification and handoff

Run focused checks during the loop, then required repository validation and relevant integration checks. Broaden according to risk and the repository policy. Report failures and checks not run.

Consider a realistic wrong branch, missing update or malformed value; the relevant test should fail under that change. Report verified behavior, commands, outcomes and material gaps.

The selected review workflow continues to own Git scope, independent review and report format.
