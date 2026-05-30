# Research Notes: Frontend Debug Workflow

Research date: 2026-05-30

## Goal

Create a frontend-focused workflow for debugging user-specified code paths and symptoms. The workflow must inspect code and nearby usage, explain why the issue happens, select the right local skills, fix the root cause, verify, and record the workflow from intake through completion.

## External Sources Checked

| Source | URL | Relevant workflow idea used |
|---|---|---|
| Claude Code common workflows | https://docs.anthropic.com/en/docs/claude-code/common-workflows | Debugging and unfamiliar-code tasks should start by exploring how files work together and tracing execution flow before editing. |
| Claude Code subagents | https://docs.anthropic.com/en/docs/claude-code/sub-agents | Specialized sub-agents are useful for isolated read-only investigation or parallel research, but the coordinator must consolidate findings. |
| Anthropic: Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | Use workflow gates for predictable processes; chain investigation, hypothesis, implementation, and verification rather than one large unstructured step. |
| Superpowers systematic-debugging | https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md | No fixes without root-cause investigation; read errors, reproduce, check changes, trace data flow, find working patterns, then fix. |
| Chrome DevTools JavaScript debugging | https://developer.chrome.com/docs/devtools/javascript/ | Reproduce the bug, pause/step through code, inspect values, then fix and verify. This maps to the browser evidence gate. |
| Chrome DevTools Console logging | https://developer.chrome.com/docs/devtools/console/log | Console errors/warnings/logs are first-class evidence and should be recorded, not paraphrased from memory. |
| Playwright Trace Viewer | https://playwright.dev/docs/trace-viewer | Recorded traces provide action timeline, snapshots, network/console context, and are useful for browser/E2E failures. |
| React Developer Tools | https://react.dev/learn/react-developer-tools | Component tree, props, state, and hooks inspection help confirm React render/state root causes. |

## Workflow Decisions

1. **User paths are starting points, not the full scope**
   - The agent must inspect the specified files plus call sites, imports, parent/child components, route/form/grid/i18n/style/API state boundaries.

2. **Root cause gate before edits**
   - The workflow borrows the `systematic-debugging` rule: do not fix until evidence supports why the issue happens.

3. **Skill selection is explicit and local**
   - Debug fixes are routed to exact local skills such as `react-useeffect`, `ag-grid`, `ant-design`, `react-hook-form-zod`, `internationalization-i18n`, `browser-testing-with-devtools`, and `verification-before-completion`.

4. **Workflow recording is required**
   - The final answer must preserve intake, evidence, hypothesis, selected skills, changed files, verification, and remaining risk so the debug run can be replayed or audited.

5. **Fixes are minimal**
   - The workflow rejects symptom masking (`as any`, blanket optional chaining, eslint disables, arbitrary timeout) unless evidence proves it is the correct pattern.
