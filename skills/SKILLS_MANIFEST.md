# Skills Manifest

Generated/updated: 2026-05-29

This directory is a project-level staging area for portable AI coding agent skills. Copy selected subdirectories from `skills/<skill-name>/` into the target agent runtime, for example `.claude/skills/<skill-name>/`, `.opencode/skills/<skill-name>/`, or another agent-specific parent directory.

Notes:
- Keep this directory flat: each installable skill lives at `skills/<skill-name>/SKILL.md`.
- `SKILLS_MANIFEST.md` is metadata only, not an installable skill.
- React Router skills are mode-specific; copy only the mode your project actually uses unless you intentionally want all modes available.
- Third-party skills were copied as-is from upstream sources; review licenses and content before publishing or vendoring into another repository.

Total installed skill directories: 65

| Category | Skill dir | Source | Commit | Source path | Why included |
|---|---|---|---|---|---|
| workflow | `using-superpowers` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/using-superpowers` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `brainstorming` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/brainstorming` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `writing-plans` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/writing-plans` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `executing-plans` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/executing-plans` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `subagent-driven-development` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/subagent-driven-development` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `dispatching-parallel-agents` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/dispatching-parallel-agents` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `test-driven-development` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/test-driven-development` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `systematic-debugging` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/systematic-debugging` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `requesting-code-review` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/requesting-code-review` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `receiving-code-review` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/receiving-code-review` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `verification-before-completion` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/verification-before-completion` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `finishing-a-development-branch` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/finishing-a-development-branch` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `using-git-worktrees` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/using-git-worktrees` | 通用 AI coding workflow / planning / TDD / debugging / review |
| workflow | `writing-skills` | https://github.com/obra/superpowers | `f2cbfbe` | `skills/writing-skills` | 通用 AI coding workflow / planning / TDD / debugging / review |
| official | `skill-creator` | https://github.com/anthropics/skills | `690f15c` | `skills/skill-creator` | 官方 skill authoring 範例 |
| official | `frontend-design` | https://github.com/anthropics/skills | `690f15c` | `skills/frontend-design` | 官方前端視覺設計 skill |
| official | `webapp-testing` | https://github.com/anthropics/skills | `690f15c` | `skills/webapp-testing` | 官方 Playwright local web app testing skill |
| official | `web-artifacts-builder` | https://github.com/anthropics/skills | `690f15c` | `skills/web-artifacts-builder` | React/Tailwind/shadcn HTML artifact 建構流程 |
| engineering-workflow | `using-agent-skills` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/using-agent-skills` | meta skill：判斷何時使用 skills |
| engineering-workflow | `spec-driven-development` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/spec-driven-development` | 重大功能前先寫 spec |
| engineering-workflow | `planning-and-task-breakdown` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/planning-and-task-breakdown` | 拆解任務與規劃 |
| engineering-workflow | `source-driven-development` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/source-driven-development` | 以官方來源/文件驅動實作決策 |
| engineering-workflow | `incremental-implementation` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/incremental-implementation` | 小步交付，避免大爆炸修改 |
| engineering-workflow | `code-review-and-quality` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/code-review-and-quality` | 多面向 code review / quality gate |
| engineering-workflow | `security-and-hardening` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/security-and-hardening` | 安全與 hardening |
| engineering-workflow | `performance-optimization` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/performance-optimization` | 效能分析與最佳化 |
| engineering-workflow | `frontend-ui-engineering` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/frontend-ui-engineering` | production-quality frontend UI engineering |
| engineering-workflow | `browser-testing-with-devtools` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/browser-testing-with-devtools` | 真瀏覽器/DevTools 驗證流程 |
| engineering-workflow | `context-engineering` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/context-engineering` | 新 session / 切任務時整理 context |
| engineering-workflow | `documentation-and-adrs` | https://github.com/addyosmani/agent-skills | `6ce0298` | `skills/documentation-and-adrs` | 文件與 ADR |
| frontend | `vercel-react-best-practices` | https://github.com/vercel-labs/agent-skills | `1801156` | `skills/react-best-practices` | Vercel React/Next.js performance best practices |
| frontend | `web-design-guidelines` | https://github.com/vercel-labs/agent-skills | `1801156` | `skills/web-design-guidelines` | Vercel Web Interface Guidelines |
| frontend | `vercel-composition-patterns` | https://github.com/vercel-labs/agent-skills | `1801156` | `skills/composition-patterns` | React composition patterns |
| frontend | `vercel-react-view-transitions` | https://github.com/vercel-labs/agent-skills | `1801156` | `skills/react-view-transitions` | React View Transition API |
| frontend-toolkit | `react-dev` | https://github.com/softaworks/agent-toolkit | `3027f20` | `skills/react-dev` | React + TypeScript component / hook patterns |
| frontend-toolkit | `react-useeffect` | https://github.com/softaworks/agent-toolkit | `3027f20` | `skills/react-useeffect` | useEffect 官方文件導向最佳實務 |
| frontend-toolkit | `design-system-starter` | https://github.com/softaworks/agent-toolkit | `3027f20` | `skills/design-system-starter` | design system starter workflow |
| frontend-toolkit | `qa-test-planner` | https://github.com/softaworks/agent-toolkit | `3027f20` | `skills/qa-test-planner` | QA / test planning |
| frontend-toolkit | `openapi-to-typescript` | https://github.com/softaworks/agent-toolkit | `3027f20` | `skills/openapi-to-typescript` | OpenAPI to TypeScript workflow |
| frontend-quality | `tailwind-design-system` | https://github.com/wshobson/agents | `05231aa` | `plugins/frontend-mobile-development/skills/tailwind-design-system` | Tailwind CSS design system |
| frontend-quality | `react-state-management` | https://github.com/wshobson/agents | `05231aa` | `plugins/frontend-mobile-development/skills/react-state-management` | React state management 選型與 patterns |
| frontend-quality | `typescript-advanced-types` | https://github.com/wshobson/agents | `05231aa` | `plugins/javascript-typescript/skills/typescript-advanced-types` | advanced TypeScript types |
| frontend-quality | `javascript-testing-patterns` | https://github.com/wshobson/agents | `05231aa` | `plugins/javascript-typescript/skills/javascript-testing-patterns` | JS/TS testing patterns |
| frontend-quality | `e2e-testing-patterns` | https://github.com/wshobson/agents | `05231aa` | `plugins/developer-essentials/skills/e2e-testing-patterns` | E2E testing patterns |
| frontend-quality | `accessibility-compliance` | https://github.com/wshobson/agents | `05231aa` | `plugins/ui-design/skills/accessibility-compliance` | accessibility / WCAG |
| frontend-quality | `design-system-patterns` | https://github.com/wshobson/agents | `05231aa` | `plugins/ui-design/skills/design-system-patterns` | design system patterns |
| frontend-quality | `responsive-design` | https://github.com/wshobson/agents | `05231aa` | `plugins/ui-design/skills/responsive-design` | responsive design patterns |
| react-router | `react-router-declarative-mode` | https://github.com/remix-run/agent-skills | `1015eb4` | `skills/react-router-declarative-mode` | React Router 官方 skill；實際移植時依專案 mode 選一個或少量使用 |
| react-router | `react-router-data-mode` | https://github.com/remix-run/agent-skills | `1015eb4` | `skills/react-router-data-mode` | React Router 官方 skill；實際移植時依專案 mode 選一個或少量使用 |
| react-router | `react-router-framework-mode` | https://github.com/remix-run/agent-skills | `1015eb4` | `skills/react-router-framework-mode` | React Router 官方 skill；實際移植時依專案 mode 選一個或少量使用 |
| antd | `ant-design` | https://github.com/ant-design/antd-skill | `e65d2d3` | `skills/ant-design` | Ant Design ecosystem 官方 skill |
| antd | `antd` | https://github.com/ant-design/antd-skill | `e65d2d3` | `skills/antd` | Ant Design offline CLI workflow |
| frontend-specific | `tailwind-v4-shadcn` | https://github.com/secondsky/claude-skills | `5e92b71` | `plugins/tailwind-v4-shadcn/skills/tailwind-v4-shadcn` | Tailwind v4 + shadcn/ui + Vite/React setup |
| frontend-specific | `react-hook-form-zod` | https://github.com/secondsky/claude-skills | `5e92b71` | `plugins/react-hook-form-zod/skills/react-hook-form-zod` | React Hook Form + Zod forms |
| frontend-specific | `internationalization-i18n` | https://github.com/secondsky/claude-skills | `5e92b71` | `plugins/internationalization-i18n/skills/internationalization-i18n` | i18next/gettext/Intl i18n workflow |
| frontend-specific | `vitest-testing` | https://github.com/secondsky/claude-skills | `5e92b71` | `plugins/vitest-testing/skills/vitest-testing` | Vitest unit/integration testing |
| testing | `playwright-best-practices` | https://github.com/currents-dev/playwright-best-practices-skill | `ef329e7` | `.` | Playwright E2E / component / visual / CI best practices |
| code-review | `code-review-excellence` | https://github.com/awesome-skills/code-review-skill | `aca7203` | `.` | React / TypeScript / CSS / architecture / performance code review |
| ag-grid | `ag-grid` | https://github.com/majiayu000/claude-skill-registry | `261ec24cb3` | `skills/development/ag-grid` | AG Grid + React + TypeScript patterns；後續可再改寫為本專案自有 skill |
| code-review | `typescript-code-reviewer` | project-curated from TypeScript official docs, typescript-eslint, OWASP, React docs, and license-clear review skills | `local-2026-05-28` | `skills/typescript-code-reviewer` | TypeScript / TSX 專用 code reviewer；未直接複製無授權的 Exploration-labs/typescript-code-review，而是整理官方與 MIT/Apache 來源 |
| web-research | `playwright-mcp-usage` | user-provided attached file | `local-2026-05-29` | `Z:/新.txt` | 一般網路搜尋被阻擋時，使用 Playwright MCP 透過真實瀏覽器做 DOM 讀取、截圖檢查與受控互動 |
| code-review | `audit-code-reviewer` | https://github.com/vosslab/vosslab-skills | `8382b5e` | `skills/audit-code-reviewer` | 平行多 reviewer audit；適合 merge/release 前讓多個 sub-agent 獨立檢查並由 coordinator 彙整 |
| security-review | `secpriv-code-review` | https://github.com/facebookresearch/secpriv-skill | `5e5c2ca` | `SKILL.md` | Meta/Facebook Research SecPriv security + privacy code review；CWE/GDPR mapping、detector-validator、confidence threshold；staged copy 加上相容 frontmatter |
| frontend-review-workflow | `frontend-staged-review-workflow` | project-curated from Anthropic Claude Code subagents docs, GitHub PR review docs, Google Engineering Practices, SmartBear review practices, and local review skills | `local-2026-05-29` | `skills/frontend-staged-review-workflow` | 前端 staged diff review workflow；只 review `git diff --cached`，每個選用 review skill 至少 2 個 sub-agent，輸出 path/severity/recommended fix，排除 unit test 建議 |
| frontend-debug-workflow | `frontend-debug-workflow` | project-curated from Claude Code common workflows/subagents docs, Anthropic Building Effective Agents, Superpowers systematic-debugging, Chrome DevTools, Playwright Trace Viewer, React DevTools, and local frontend skills | `local-2026-05-30` | `skills/frontend-debug-workflow` | 前端 debug workflow；使用者提供 code paths + problem 後，讀指定檔案與附近使用、收集 evidence、形成 root cause hypothesis、選 exact local skills、最小修正並驗證紀錄 |
