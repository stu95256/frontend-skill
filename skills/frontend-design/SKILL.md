---
name: frontend-design
description: Design or refine frontend interfaces with visual direction matched to their task. Use for new pages, redesigns, dashboards, reading surfaces, critique and polish while preserving product content, behavior and the existing design system.
license: Apache-2.0; see LICENSE.impeccable and LICENSE.txt
metadata:
  primary-source: https://github.com/pbakaus/impeccable
  primary-source-commit: 8409a564d1baee90b2dde4f7a8f06288838e3921
  primary-source-path: .github/skills/impeccable
  retained-source: https://github.com/anthropics/skills
  retained-source-commit: dbd4588f9e1033efb41dad4bef2f7947c8993d44
  adaptation: Document-only design playbooks without launchers, hooks or extra agents
---

# Frontend Design

Choose direction from the brief, audience and job of this surface. Existing product truth, content and tokens constrain the work. Refinement preserves identity; a requested redesign can replace the visual world.

Read existing product/design documentation when relevant. A missing design document does not make an established app a blank slate. Do not change configuration or create documentation just to satisfy this Skill.

## Surface modes

| Mode | Visitor's task | Design emphasis |
|---|---|---|
| Persuade | Decide and act on a landing/pricing/campaign page | Distinct direction, credible content and a clear action |
| Operate | Work in a dashboard, editor, admin or settings surface | Familiar controls, scanability, density and consistent states |
| Read | Understand documentation, guides or articles | Hierarchy, readable measure and navigation |
| Experience | Explore a portfolio, gallery or expressive work | Let the artifact lead |

Choose per surface: a tool's landing page and dashboard have different jobs. Read [surface modes](references/surface-modes.md) when these tradeoffs matter.

## Build or refine

1. Inspect target and surrounding components, real content, fonts, tokens and assets.
2. For new work, outline palette, type, hierarchy and layout. Narrow polish proceeds from the incumbent design.
3. Check against the brief. Generic card grids, decorative statistics and a habitual palette are not subject-specific choices.
4. Implement working controls and necessary pending, empty and error states.
5. Critique against [design quality](references/design-quality.md), then run relevant type/build and unit/DOM checks. State their visual limits.

Use supplied images and committed references as evidence after checking version/theme relevance. Do not invent visual observations from source code.

## Preserve intent

- Pinned style wins over aesthetic preferences and anti-pattern lists.
- Follow existing components and tokens unless the approved change requires otherwise.
- Give the important element strongest emphasis. Consistency and readable density are deliberate choices on an Operate surface.
- Use real content; invent no customers, testimonials, prices or statistics.
- Controls name actions, errors explain recovery and empty states offer a next step.
- Preserve responsive structure and ordinary native control behavior.
- Motion belongs only when it serves the requested interaction; do not introduce a separate optimization workflow.

For critique, give location, impact and concrete improvement in importance order. Polish stays within the requested surface and preserves behavior. Redesign explains the intended hierarchy.

This document-only adaptation requires no executable launcher, hooks, additional agents, external service or live-page tooling.
