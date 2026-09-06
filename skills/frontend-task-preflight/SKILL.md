---
name: frontend-task-preflight
description: Use before implementing frontend tasks, especially React, TypeScript, Tailwind, AG Grid React, Ant Design, react-i18next,
  react-router-dom, react-hook-form, or Figma/design-to-code tasks.
license: Local project documentation
---

# Frontend Task Preflight

Use this skill before writing code for frontend implementation tasks.

Preferred VS Code entry point: select the **Frontend Task Preflight** custom agent. It owns the `agent` tool, explicitly allows `Frontend Researcher` and `Frontend Plan Reviewer`, and exposes a user-visible handoff to **Frontend Implementation**. If this skill loads in another top-level agent, use `#tool:agent/runSubagent` with named or anonymous read-only workers.

## Non-negotiables

- Do not edit source code during preflight.
- Do not scaffold files during preflight.
- First understand the user's goal, relevant code, Figma/design input, current product behavior, and constraints.
- Read relevant code and nearby patterns before asking the user questions.
- Treat Figma as input, not the only truth.
- If Figma/design and current code differ, produce a gap matrix instead of assuming either side is correct.
- Ask only blocking questions that affect scope, UX, architecture, data flow, validation, accessibility, or verification; user-facing questions must be written in Chinese, while code identifiers, paths, commands, enum values, API fields, and quoted source text may remain unchanged.
- Present approach options and tradeoffs before implementation.
- Write an implementation plan with exact files, steps, verification commands, expected results, risks, and assumptions.
- Include a naming plan for generated code: variable and function names must be descriptive and domain-specific, avoid abbreviations, and preserve important qualifiers from existing code or business concepts. For example, do not shorten `isSpcTableEmptyVal` to `isEmptyVal`.
- Start implementation only after the user explicitly approves the plan.

## Workflow

1. Intake
2. Brainstorming / problem framing
3. Skill selection
4. Code reconnaissance
5. Figma/design reconnaissance
6. Gap analysis
7. Unknowns and clarifying questions
8. External research
9. Approach options
10. User discussion / decision
11. Implementation plan
12. Plan self-review
13. Plan review, if complex
14. Final handoff

## Required output

Return these sections when applicable:

- Intake Summary
- Brainstorming Notes
- Skill Selection
- Code Reconnaissance
- Design / Figma Reconnaissance
- Gap Matrix
- Clarifying Questions
- External Research
- Approach Options
- Implementation Plan
- Naming Plan
- Plan Self-review
- Final Handoff

## Full workflow reference

Read the full workflow for detailed templates, sub-agent prompts, gates, and Definition of Done:

`references/FRONTEND_TASK_PREFLIGHT_WORKFLOW.md`

For the guided VS Code Chat experience, select the **Frontend Task Preflight** custom agent from `~/.copilot/agents/frontend-task-preflight.agent.md`.
