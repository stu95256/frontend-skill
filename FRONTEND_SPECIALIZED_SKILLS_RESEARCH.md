# 前端專用 Skill 調查紀錄

最後調查日期：2026-05-28

本檔案紀錄 React、TypeScript、Tailwind、AG Grid React、Ant Design、react-i18next、react-router-dom、react-hook-form 等前端專案會用到的專用 Agent / Claude / Hermes skills。
2026-05-28 起，已將本檔推薦的核心前端 skills 下載到 `skills/` staging 目錄；完整下載清單請看 `skills/SKILLS_MANIFEST.md`。

## 本次有回頭查看的網頁與來源

| 來源 | URL | 本次觀察 |
|---|---|---|
| Awesome Frontend Agent Skills | https://github.com/finfin/awesome-frontend-skills | 這次最重要的前端索引；已看到 React、TypeScript、Tailwind、React Router、shadcn、Testing、Web Quality 等分類，且多數附 `npx skills add` 指令。 |
| Awesome Claude Skills | https://github.com/travisvn/awesome-claude-skills | 綜合索引；前端相關主要集中在 Anthropic 官方 `frontend-design`、`webapp-testing`、`web-artifacts-builder` 與 shadcn/ui。 |
| shadcn/ui Skills 文件 | https://ui.shadcn.com/docs/skills | 官方 shadcn skill / workflow，描述可讓 AI assistant 取得 shadcn/ui components、patterns、best practices。 |
| SkillsMP | https://skillsmp.com/ | 可查到 `ag-grid-patterns`、`react-hook-form` 等 marketplace 條目；適合補找非官方或小眾 skill。 |
| MCPMarket Skills | https://mcpmarket.com/tools/skills | 查詢時部分頁面遇到 429 Too Many Requests；搜尋結果仍顯示 React Hook Form、i18n、Ant Design Vue 等條目，之後可再查。 |
| Claude Bazaar | https://claudebazaar.com/ | 查到 Ant Design skill 條目，指向 `ant-design/antd-skill`。 |
| AG Grid MCP Server 官方文件 | https://www.ag-grid.com/javascript-data-grid/mcp-server/ | 不是 SKILL.md，但 AG Grid 官方提供 MCP Server，可補強 AI 查詢 AG Grid 文件與 API 的能力。 |
| i18n-agent/i18n-skills | https://github.com/i18n-agent/i18n-skills | 不是標準 SKILL.md，而是 Claude Code slash commands；支援 React/Vue/Angular/Svelte 等 codebase 的 i18n audit / wrapping。 |

## 本專案技術棧對應推薦清單

| 類別 | Skill / 資源 | 來源 | 摘要 | 安裝 / 取得 |
|---|---|---|---|---|
| React | `vercel-react-best-practices` | https://github.com/vercel-labs/agent-skills | Vercel Engineering 的 React / Next.js performance guidelines；適合寫、review、refactor React code，避免 waterfall、bundle、re-render 等效能問題。 | `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices` |
| React | `react-dev` | https://github.com/softaworks/agent-toolkit | React + TypeScript type-safe component patterns、hook typing、event typing、generic components、React 18/19 patterns。 | `npx skills add softaworks/agent-toolkit --skill react-dev` |
| React | `react-useeffect` | https://github.com/softaworks/agent-toolkit | 官方 docs 取向的 `useEffect` 最佳實務；強調何時不要用 Effect，以及 data fetching / state sync 的替代方案。 | `npx skills add softaworks/agent-toolkit --skill react-useeffect` |
| React | `react-expert` | https://github.com/Jeffallan/claude-skills | React 18+ / JSX / TSX / custom hooks / rendering debugging / class-to-function migration / performance / React 19 features。 | `npx skills add Jeffallan/claude-skills --skill react-expert` |
| React | `react-state-management` | https://github.com/wshobson/agents | Redux Toolkit、Zustand、Jotai、React Query、URL state 等選型與 patterns。 | `npx skills add wshobson/agents --skill react-state-management` |
| React | `react-doctor` | https://github.com/millionco/react-doctor | React codebase quality / performance / security / architecture scanner；Awesome Frontend 清單描述可輸出 0–100 score 與 actionable diagnostics。 | `npx skills add millionco/react-doctor --skill react-doctor` |
| TypeScript | `typescript-clean-code` | https://github.com/bmad-labs/skills | TypeScript clean code patterns、架構慣例、refactoring、PR review 原則。 | `npx skills add bmad-labs/skills --skill typescript-clean-code` |
| TypeScript | `typescript-advanced-types` | https://github.com/wshobson/agents | Generics、conditional types、mapped types、template literal types、utility types；適合複雜 reusable type utility。 | `npx skills add wshobson/agents --skill typescript-advanced-types` |
| TypeScript | `typescript-pro` | https://github.com/Jeffallan/claude-skills | Advanced TypeScript type systems、custom type guards、utility types、branded types、discriminated unions、monorepo / tRPC 類型安全。 | `npx skills add Jeffallan/claude-skills --skill typescript-pro` |
| TypeScript | `typescript-unit-testing` | https://github.com/bmad-labs/skills | TypeScript unit testing；原 skill 偏 NestJS/Jest，但 AAA、mocking、coverage、flaky/open handles debugging 仍可參考。 | `npx skills add bmad-labs/skills --skill typescript-unit-testing` |
| TypeScript | `typescript-e2e-testing` | https://github.com/bmad-labs/skills | TypeScript E2E / integration testing；原 skill 偏 backend infra，但 Given-When-Then、test isolation、flaky debugging 可參考。 | `npx skills add bmad-labs/skills --skill typescript-e2e-testing` |
| TypeScript / Code review | `typescript-code-reviewer` | 本專案 `skills/typescript-code-reviewer`，研究來源見 `skills/typescript-code-reviewer/references/research-sources.md` | TypeScript / TSX 專用 reviewer workflow；檢查 strict tsconfig、`any`/`unknown`、unsafe assertions、async/error、React hooks/props、XSS、runtime validation、tests。 | 已下載/建立於 `skills/typescript-code-reviewer/`；可複製到 `.claude/skills/`、`.opencode/skills/`、`.agents/skills/`。 |
| Tailwind / shadcn | `tailwind-design-system` | https://github.com/wshobson/agents | Tailwind CSS v4、design tokens、component libraries、responsive patterns；適合建立設計系統。 | `npx skills add wshobson/agents --skill tailwind-design-system` |
| Tailwind / shadcn | `tailwind-v4-shadcn` | https://github.com/secondsky/claude-skills | Tailwind v4 + shadcn/ui + Vite + React production setup；含 `@theme inline`、CSS variables、dark mode、v3→v4 migration gotchas。 | `/plugin install tailwind-v4-shadcn@claude-skills` 或 `npx skills add secondsky/claude-skills --skill tailwind-v4-shadcn` |
| Tailwind / shadcn | `shadcn` official skill | https://ui.shadcn.com/docs/skills | shadcn/ui 官方 skills；提供 components、patterns、best practices、CLI workflow、component composition rules。 | `npx shadcn@latest add skills` |
| Tailwind / shadcn | `shadcn-ui` | https://github.com/jezweb/claude-skills | React 專案安裝與設定 shadcn/ui components；涵蓋 forms、data tables、navigation、modals、semantic tokens。 | `npx skills add jezweb/claude-skills --skill shadcn-ui` |
| Tailwind / UI | `frontend-design` | https://github.com/anthropics/skills | Anthropic 官方 frontend design skill；用於 dashboard、React components、HTML/CSS layout，避免 generic AI aesthetics。 | `npx skills add anthropics/skills --skill frontend-design` |
| React Router | `react-router-framework-mode` | https://github.com/remix-run/agent-skills | React Router 官方 skill；framework mode、loaders、actions、forms、pending/optimistic UI、error boundaries。 | `npx skills add remix-run/agent-skills --skill react-router-framework-mode` |
| React Router | `react-router-data-mode` | https://github.com/remix-run/agent-skills | React Router data mode；`createBrowserRouter`、`RouterProvider`、route objects、loaders/actions、`useFetcher`。 | `npx skills add remix-run/agent-skills --skill react-router-data-mode` |
| React Router | `react-router-declarative-mode` | https://github.com/remix-run/agent-skills | React Router declarative mode；`BrowserRouter`、JSX routes、`Link/NavLink`、URL params、search params。 | `npx skills add remix-run/agent-skills --skill react-router-declarative-mode` |
| AG Grid React | `ag-grid` | https://github.com/majiayu000/claude-skill-registry | AG Grid + React + TypeScript；涵蓋 configuration、accessibility、column definitions、cell renderers、performance。 | 複製 `skills/development/ag-grid/SKILL.md`；未看到通用 `npx skills add` 指令。 |
| AG Grid React | `ag-grid-patterns` | https://skillsmp.com/skills/creatifcoding-gbg-packages-tmnl-claude-skills-ag-grid-patterns-skill-md | SkillsMP 條目；AG-Grid v34 integration patterns、custom cell renderers、themes、grid UI。注意描述中出現 TMNL 專案脈絡，可能需要改寫才能通用化。 | `npx skills add creatifcoding/gbg` |
| AG Grid React | AG Grid MCP Server | https://www.ag-grid.com/javascript-data-grid/mcp-server/ | 官方 MCP Server，不是 skill；可讓 agent 查 AG Grid docs / API，之後若常寫 AG Grid 值得研究。 | 依官方 MCP 文件設定。 |
| Ant Design | `ant-design` | https://github.com/ant-design/antd-skill | 官方 Ant Design ecosystem skill；antd v6、Ant Design Pro 5、ProComponents、Ant Design X v2、component selection、tokens、SSR、a11y、performance、migration。 | `npx skills add ant-design/antd-skill --skill ant-design` |
| Ant Design | `antd` | https://github.com/ant-design/antd-skill | 官方 offline Ant Design CLI workflow；API lookup、debugging、migration、usage analysis；允許 `antd` CLI 查 props/tokens/demos。 | `npx skills add ant-design/antd-skill --skill antd` |
| react-i18next / i18n | `internationalization-i18n` | https://github.com/secondsky/claude-skills | 使用 i18next、gettext、Intl API 建立 multi-language support、translation workflow、RTL、date/currency formatting。 | `/plugin install internationalization-i18n@claude-skills` 或 `npx skills add secondsky/claude-skills --skill internationalization-i18n` |
| react-i18next / i18n | `i18n` slash commands | https://github.com/i18n-agent/i18n-skills | Claude Code slash commands；可 audit hardcoded strings、split sentence、plural、unused keys、missing `t()` 等。不是標準 SKILL.md，但非常適合 i18n QA。 | `cp -r commands/*.md ~/.claude/commands/` |
| react-hook-form | `react-hook-form-zod` | https://github.com/secondsky/claude-skills | React Hook Form + Zod；form schemas、field arrays、multi-step forms、resolver issues、nested validation、shadcn form。 | `/plugin install react-hook-form-zod@claude-skills` 或 `npx skills add secondsky/claude-skills --skill react-hook-form-zod` |
| react-hook-form | `react-hook-form` | https://github.com/claude-dev-suite/claude-dev-suite | React Hook Form + Zod validation；form setup、validation schema、field components、error handling、submission、shadcn/ui integration。 | `npx skills add claude-dev-suite/claude-dev-suite --skill react-hook-form` |
| Testing / Browser | `webapp-testing` | https://github.com/anthropics/skills | Anthropic 官方 Playwright local web app testing；可驗證 frontend functionality、UI behavior、screenshots、browser logs。 | `npx skills add anthropics/skills --skill webapp-testing` |
| Testing / Browser | `playwright-best-practices` | https://github.com/currents-dev/playwright-best-practices-skill | Playwright E2E、component、API、visual regression、a11y、CI、fixtures、mocking、auth、flaky debugging。 | `npx skills add currents-dev/playwright-best-practices-skill` |
| Testing / Browser | `playwright-expert` | https://github.com/Jeffallan/claude-skills | Playwright E2E test infrastructure、page objects、fixtures、reporters、CI、API mocking、visual regression、flaky tests。 | `npx skills add Jeffallan/claude-skills --skill playwright-expert` |
| Testing / Unit | `vitest-testing` | https://github.com/secondsky/claude-skills | Vitest for TypeScript/JavaScript；unit/integration tests、native ESM、Vite-powered testing、mocking。 | `/plugin install vitest-testing@claude-skills` 或 `npx skills add secondsky/claude-skills --skill vitest-testing` |
| Web Quality | `web-quality` | https://github.com/addyosmani/web-quality-skills | Lighthouse、Core Web Vitals、performance、accessibility WCAG、SEO、best practices；支援 React/Vue/Angular/Svelte/Next/Nuxt/Astro。 | `npx skills add addyosmani/web-quality-skills` |
| UI Review | `web-design-guidelines` | https://github.com/vercel-labs/agent-skills | Vercel Web Interface Guidelines；適合 review UI、accessibility、UX、design audit。 | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` |
| Code Review | `code-review-skill` | https://github.com/awesome-skills/code-review-skill | 包含 React 19、TypeScript、CSS、architecture、performance 的 review guide；適合作為 merge 前檢查。 | `git clone https://github.com/awesome-skills/code-review-skill ~/.claude/skills/code-review-skill` |

## 依本專案的優先級建議

### A. 最高優先：直接對應目前技術棧

1. React：`vercel-react-best-practices`、`react-dev`、`react-useeffect`、`react-expert`
2. TypeScript：`typescript-clean-code`、`typescript-advanced-types`、`typescript-pro`、`typescript-code-reviewer`
3. Tailwind / UI：`tailwind-design-system`、`tailwind-v4-shadcn`、shadcn 官方 skill、`frontend-design`
4. React Router：依專案實際模式選 `react-router-declarative-mode` 或 `react-router-data-mode`；若走 full-stack framework mode 才用 `react-router-framework-mode`
5. Ant Design：官方 `ant-design` + `antd`
6. react-hook-form：`react-hook-form-zod` 或 `react-hook-form`
7. react-i18next：`internationalization-i18n` + `i18n-agent/i18n-skills` commands
8. AG Grid：`ag-grid` + AG Grid 官方 MCP Server；`ag-grid-patterns` 可參考但要注意其專案特化內容

### B. 品質保證組合

1. `webapp-testing`：本地前端功能、console、browser logs、screenshots
2. `playwright-best-practices` 或 `playwright-expert`：建立 / review E2E 測試
3. `vitest-testing`：單元測試與 integration tests
4. `web-quality`：Lighthouse / Core Web Vitals / a11y / SEO
5. `web-design-guidelines`：UI / UX / accessibility review
6. `code-review-skill`：React / TypeScript / CSS / architecture / performance code review

### C. 之後如果只想先裝最少組合

如果之後要實際下載或安裝，建議先從這 10 個開始：

1. `anthropics/skills --skill frontend-design`
2. `anthropics/skills --skill webapp-testing`
3. `vercel-labs/agent-skills --skill vercel-react-best-practices`
4. `softaworks/agent-toolkit --skill react-dev`
5. `softaworks/agent-toolkit --skill react-useeffect`
6. `wshobson/agents --skill tailwind-design-system`
7. `remix-run/agent-skills --skill react-router-declarative-mode` 或 `react-router-data-mode`
8. `ant-design/antd-skill --skill ant-design`
9. `secondsky/claude-skills --skill react-hook-form-zod`
10. `secondsky/claude-skills --skill internationalization-i18n`

AG Grid 因為目前找到的來源較少，建議獨立整理成專案自有 skill，並搭配 AG Grid 官方 MCP Server 或官方文件。

## 已下載到 `skills/` staging 的前端核心集合

2026-05-28 已下載/建立 60 個可移植 skill 目錄，其中前端與品質保證重點包含：

- React：`vercel-react-best-practices`、`react-dev`、`react-useeffect`、`react-state-management`
- TypeScript：`typescript-advanced-types`、`openapi-to-typescript`、`typescript-code-reviewer`
- Tailwind / UI：`tailwind-design-system`、`tailwind-v4-shadcn`、`frontend-design`、`web-design-guidelines`、`design-system-patterns`、`responsive-design`
- React Router：`react-router-declarative-mode`、`react-router-data-mode`、`react-router-framework-mode`（移植時依專案模式選用）
- Ant Design：`ant-design`、`antd`
- react-hook-form：`react-hook-form-zod`
- i18n：`internationalization-i18n`
- AG Grid：`ag-grid`
- Testing / Quality：`webapp-testing`、`playwright-best-practices`、`vitest-testing`、`browser-testing-with-devtools`、`frontend-ui-engineering`、`accessibility-compliance`
- Code review：`code-review-and-quality`、`code-review-excellence`、`typescript-code-reviewer`

完整來源、commit 與原始路徑請看 `skills/SKILLS_MANIFEST.md`；驗證結果請看 `skills/VALIDATION_REPORT.md`。

## 需要注意的點

1. 有些 marketplace 條目不是官方來源，要讀 `SKILL.md` 內容並確認授權、維護狀態與是否過度專案特化。
2. `wshobson/agents` 的 skills 分散在 `plugins/*/skills/*/SKILL.md`，安裝前要先確認實際路徑與 skill name。
3. `secondsky/claude-skills` 使用 Claude plugin marketplace 格式；也可能可用 `npx skills add`，但實際下載前建議先用 `--list` 驗證。
4. `i18n-agent/i18n-skills` 是 slash commands，不是標準 Agent Skill；可以記錄但不要混淆。
5. `AG Grid MCP Server` 是 MCP，不是 skill；用途是提供工具 / 文件查詢能力，不是 procedural SKILL.md。
6. `bmad-labs` 的 TypeScript testing skills 偏 NestJS/backend，若本專案是純前端，使用時要抽取 testing workflow，不要照抄 backend infra。
7. React Router 要先確認專案使用 declarative mode、data mode 還是 framework mode；不要一次混用三種 Router skill。

## 後續搜尋關鍵字

```text
filename:SKILL.md React TypeScript frontend
filename:SKILL.md react-useeffect
filename:SKILL.md tailwind shadcn vite react
filename:SKILL.md react-router BrowserRouter
filename:SKILL.md react-router data mode
filename:SKILL.md react-hook-form zod
filename:SKILL.md i18next react-i18next
filename:SKILL.md ag-grid react typescript
filename:SKILL.md antd Ant Design
"AG Grid" "Claude Code Skill"
"Ant Design" "npx skills add"
"react-hook-form" "npx skills add"
"i18next" "Claude Code skill"
```
