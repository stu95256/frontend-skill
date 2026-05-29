# Skill 來源清單

最後搜尋日期：2026-05-28

本檔案用來紀錄之後可下載、研究或轉換成前端 AI coding skill 的常見來源。
專案目標偏向提升 AI 撰寫前端的能力，優先關注 React、TypeScript、Tailwind、AG Grid React、Ant Design、react-i18next、react-router-dom、react-hook-form。

## 下載方式常用指令

### 使用 Vercel Skills CLI

很多新版 Agent Skill repository 都支援 `npx skills add`：

```bash
# 列出某個 repo 內可安裝的 skills
npx skills add <owner/repo> --list

# 安裝指定 skill
npx skills add <owner/repo> --skill <skill-name>

# 安裝到指定 agent
npx skills add <owner/repo> --skill <skill-name> -a claude-code -a cursor

# 安裝 repo 內全部 skills
npx skills add <owner/repo> --all
```

### 直接用 Git 下載

```bash
# 下載整個 repository
git clone https://github.com/<owner>/<repo>.git

# 只想取其中 skills 目錄時，可使用 sparse checkout
git clone --depth 1 --filter=blob:none --sparse https://github.com/<owner>/<repo>.git
cd <repo>
git sparse-checkout set skills
```

## 優先入口網站與目錄

| 來源 | URL | 用途 |
|---|---|---|
| Claude Code Skills 官方文件 | https://code.claude.com/docs/en/skills | Claude Code skill 的官方說明、安裝位置與使用方式 |
| Anthropic Agent Skills 官方 repo | https://github.com/anthropics/skills | 官方 skill 範例、spec、template；含 `frontend-design`、`webapp-testing`、`web-artifacts-builder` |
| Vercel Skills CLI | https://github.com/vercel-labs/skills | `npx skills add` 工具來源；適合批次安裝 GitHub 上的 skills |
| Awesome Frontend Agent Skills | https://github.com/finfin/awesome-frontend-skills | 前端專用 skill 清單，含 React、Tailwind、React Router、TypeScript、測試、UI library 等分類；多數附 install 指令 |
| Awesome Claude Skills | https://github.com/travisvn/awesome-claude-skills | Claude Skills 綜合索引，可用來找更多通用與工程類 skill |
| Claude Skills Library | https://claudeskills.club/ | Claude / Codex / Cursor skill marketplace 類型網站 |
| SkillsMP | https://skillsmp.com/ | Agent skills marketplace，可搜尋 Claude、Codex、ChatGPT 相關 skill |
| LobeHub Skills | https://lobehub.com/skills | Skill marketplace / directory，可用關鍵字找特定技能 |
| MCPMarket Skills | https://mcpmarket.com/tools/skills | Skill directory，搜尋前端、TypeScript、React 相關 skill |
| shadcn/ui Skills 文件 | https://ui.shadcn.com/docs/skills | shadcn 官方 skill / workflow，對 Tailwind + component composition 很有幫助 |

> 2026-05-29 補充：任務前期 workflow（目標 + 程式碼 + Figma 落差 + sub-agent + research + planning + plan review）已整理到 `FRONTEND_TASK_PREFLIGHT_WORKFLOW.md`，之後可轉成 `frontend-task-preflight` 類型 skill。
>
> 2026-05-28 補充：前端專用詳細調查已拆到 `FRONTEND_SPECIALIZED_SKILLS_RESEARCH.md`，包含 React、TypeScript、Tailwind、AG Grid、Ant Design、i18n、React Router、React Hook Form 等對應 skill。
>
> 2026-05-28 下載紀錄：已將推薦 skills 下載到專案 `skills/` staging 目錄。完整清單、來源 commit 與移植說明請看 `skills/SKILLS_MANIFEST.md`；驗證結果請看 `skills/VALIDATION_REPORT.md`。

## 推薦先追蹤的 GitHub repositories

| Repository | 重點 | 下載 / 安裝提示 |
|---|---|---|
| https://github.com/anthropics/skills | 官方 Agent Skills；可先看 `skills/frontend-design`、`skills/webapp-testing`、`skills/web-artifacts-builder` | `npx skills add anthropics/skills --list` |
| https://github.com/vercel-labs/agent-skills | Vercel 官方 agent skills；React best practices、web design guidelines、React transitions、Vercel optimization | `npx skills add vercel-labs/agent-skills --list` |
| https://github.com/addyosmani/agent-skills | Production-grade engineering skills；前端 UI engineering、browser testing、performance、TDD、code review | `npx skills add addyosmani/agent-skills --skill frontend-ui-engineering` |
| https://github.com/addyosmani/web-quality-skills | Web quality、Lighthouse、Core Web Vitals、accessibility、SEO、performance | `npx skills add addyosmani/web-quality-skills` |
| https://github.com/finfin/awesome-frontend-skills | 前端 skill curated list；最適合當作後續下載索引 | 先讀 README，再依表格的 `npx skills add ...` 安裝 |
| https://github.com/jezweb/claude-skills | Claude Code CLI skills；含 React/Tailwind、design loop、design review、design system、landing page、Vitest、UX audit | `npx skills add jezweb/claude-skills --list` |
| https://github.com/Jeffallan/claude-skills | Full-stack developer skills；有 `react-expert`、`typescript-pro`、`javascript-pro`、`nextjs-developer`、`playwright-expert` | `npx skills add Jeffallan/claude-skills --list` |
| https://github.com/softaworks/agent-toolkit | 多種 coding-agent skills；含 `react-dev`、`react-useeffect`、`mui`、`openapi-to-typescript`、design-system starter | `npx skills add softaworks/agent-toolkit --skill react-dev` |
| https://github.com/remix-run/agent-skills | React Router 官方相關 skills；包含 framework/data/declarative mode | `npx skills add remix-run/agent-skills --skill react-router-framework-mode` |
| https://github.com/bmad-labs/skills | TypeScript clean code、unit testing、E2E testing、UI/UX skill | `npx skills add bmad-labs/skills --list` |
| https://github.com/wshobson/agents | 多 agent/plugin marketplace；skill 分散在 `plugins/*/skills`，含 React state management、Tailwind design system、UI design、accessibility | 先用 GitHub 搜尋 repo 內 `SKILL.md`，再挑選下載 |
| https://github.com/awesome-skills/code-review-skill | Code review skill；含 React、TypeScript、CSS、architecture、performance guide | `git clone https://github.com/awesome-skills/code-review-skill ~/.claude/skills/code-review-skill` |
| https://github.com/Exploration-labs/typescript-code-review | 專門 TypeScript code review skill；`name: typescript-code-review`，但未找到 LICENSE | 只記錄/參考，不直接複製到本專案；本專案改建立 MIT 的 `skills/typescript-code-reviewer` |
| https://github.com/millionco/react-doctor | React codebase 檢查工具與 skill；偏向品質、效能、安全、架構診斷 | `npx skills add millionco/react-doctor --skill react-doctor` |
| https://github.com/NousResearch/hermes-agent | Hermes Agent 內建 skills；可參考 `skills/software-development`、`skills/creative`、`skills/dogfood` 等 | 直接讀 `skills/` 目錄，挑選可移植內容 |
| https://github.com/0xNyk/awesome-hermes-agent | Hermes Agent 生態的 curated list | 作為 Hermes 相關 skill / tool 索引 |

## 依本專案技術棧的優先下載方向

### React

優先來源：

- `vercel-labs/agent-skills`：`react-best-practices`
- `softaworks/agent-toolkit`：`react-dev`、`react-useeffect`
- `Jeffallan/claude-skills`：`react-expert`
- `wshobson/agents`：`react-state-management`
- `millionco/react-doctor`：`react-doctor`

### TypeScript

優先來源：

- `bmad-labs/skills`：`typescript-clean-code`、`typescript-unit-testing`、`typescript-e2e-testing`
- `Jeffallan/claude-skills`：`typescript-pro`
- `SpillwaveSolutions/mastering-typescript-skill`：`mastering-typescript`
- `wshobson/agents`：`typescript-advanced-types`

### Tailwind

優先來源：

- `wshobson/agents`：`tailwind-design-system`
- `jezweb/claude-skills`：Tailwind / shadcn 相關 skills
- `shadcn/ui` 官方 skills 文件：https://ui.shadcn.com/docs/skills
- `anthropics/skills`：`frontend-design`

### React Router

優先來源：

- `remix-run/agent-skills`：`react-router-framework-mode`、`react-router-data-mode`、`react-router-declarative-mode`

### UI / Design / Accessibility / Testing

優先來源：

- `anthropics/skills`：`frontend-design`、`webapp-testing`
- `addyosmani/agent-skills`：`frontend-ui-engineering`、`browser-testing-with-devtools`
- `addyosmani/web-quality-skills`：performance、accessibility、SEO、Core Web Vitals
- `vercel-labs/agent-skills`：`web-design-guidelines`
- `Jeffallan/claude-skills`：`playwright-expert`

## 2026-05-28 補充找到的專用來源

先前列為「尚未找到普遍流通專用 skill」的項目，本次已找到一些可追蹤來源：

| 技術 | 已找到來源 | 備註 |
|---|---|---|
| AG Grid React | `majiayu000/claude-skill-registry` 的 `skills/development/ag-grid/SKILL.md`、SkillsMP 的 `ag-grid-patterns`、AG Grid 官方 MCP Server | `ag-grid-patterns` 似乎有特定專案脈絡；AG Grid 官方 MCP Server 不是 skill，但可補強文件/API 查詢。 |
| Ant Design / Antd | https://github.com/ant-design/antd-skill | 官方 skill；包含 `ant-design` 與 `antd` 兩個 skill，涵蓋 antd v6、ProComponents、Ant Design X、offline CLI workflow。 |
| react-i18next / i18n | `secondsky/claude-skills` 的 `internationalization-i18n`、https://github.com/i18n-agent/i18n-skills | 前者是 i18next/gettext/Intl 類 skill；後者是 slash commands，不是標準 SKILL.md。 |
| react-hook-form | `secondsky/claude-skills` 的 `react-hook-form-zod`、`claude-dev-suite/claude-dev-suite` 的 `react-hook-form` | 都偏 React Hook Form + Zod + shadcn/ui forms。 |

詳細表格、安裝提示與優先級請看 `FRONTEND_SPECIALIZED_SKILLS_RESEARCH.md`。


## 2026-05-28 TypeScript code reviewer 補充調查

本次確認本專案原本沒有 top-level `skills/<name>/SKILL.md` 形式的 TypeScript 專用 reviewer；只有通用 review skills 與 TypeScript advanced types。網路上找到 `Exploration-labs/typescript-code-review` / `jdevera/agent-skills` 的 dedicated `typescript-code-review` SKILL.md，但沒有明確 LICENSE，因此未直接複製。

已建立本專案自有 `skills/typescript-code-reviewer/`，內容依官方 TypeScript / typescript-eslint / ESLint / React / OWASP 文件，以及 MIT/Apache-2.0 的 code review skills 整理。詳細來源、commit 與 caveat 見 `skills/typescript-code-reviewer/references/research-sources.md`。

## 後續搜尋關鍵字

可定期用下列關鍵字搜尋 GitHub 或搜尋引擎：

```text
"SKILL.md" React TypeScript
"SKILL.md" Tailwind React
"Claude Skills" React TypeScript
"Agent Skills" frontend React
"npx skills add" React
"npx skills add" Tailwind
"react-router" "SKILL.md"
"react-hook-form" "SKILL.md"
"react-i18next" "SKILL.md"
"ag-grid" "SKILL.md"
"Ant Design" "SKILL.md"
"typescript-code-review" "SKILL.md"
"TypeScript" "code review" "SKILL.md"
```

GitHub 搜尋也可用：

```text
filename:SKILL.md React TypeScript frontend
filename:SKILL.md Tailwind React
filename:SKILL.md react-router
filename:SKILL.md react-hook-form
filename:SKILL.md ag-grid
filename:SKILL.md antd
filename:SKILL.md "typescript-code-review"
filename:SKILL.md "TypeScript" "code review"
```

注意：GitHub code search API 通常需要登入或 token；若 CLI 搜尋失敗，可改用 GitHub 網頁搜尋。
