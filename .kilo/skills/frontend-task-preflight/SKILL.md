---
name: frontend-task-preflight
description: Use before implementing frontend tasks, especially React, TypeScript, Tailwind, AG Grid React, Ant Design, react-i18next, react-router-dom, react-hook-form, or Figma/design-to-code tasks.
version: 1.0.0
author: Local project workflow
license: Local project documentation
metadata:
  hermes:
    tags: [frontend, planning, figma, react, typescript, tailwind, ant-design, ag-grid, i18n, forms, kilo]
    related_skills: [playwright-mcp-usage, react-dev, typescript-code-reviewer, frontend-ui-engineering, accessibility-compliance, responsive-design, qa-test-planner]
---

# Frontend Task Preflight

Use this skill before writing code for frontend implementation tasks.

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

## Kilo Code usage

If this skill is installed globally for Kilo Code, pair it with the global rule file:

`~/.kilo/rules/frontend-preflight.md`

The Kilo global config should point `skills.paths` at:

`~/.kilo/skills`

and `instructions` at:

`~/.kilo/rules/*.md`

## Full workflow reference

Read the full workflow for detailed templates, sub-agent prompts, gates, and Definition of Done:

`references/FRONTEND_TASK_PREFLIGHT_WORKFLOW.md`

If the skill is moved to the planned global folder, the same full workflow should also exist at:

`~/.kilo/workflows/FRONTEND_TASK_PREFLIGHT_WORKFLOW.md`
