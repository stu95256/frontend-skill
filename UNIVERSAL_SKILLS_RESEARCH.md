# 通用 Skill 調查紀錄

最後調查日期：2026-05-27

本檔案紀錄網路上推薦、大量使用或值得優先研究的通用 Agent / Claude / Hermes Skills。
2026-05-28 起，已將本檔推薦的核心通用 workflow skills 下載到 `skills/` staging 目錄；完整下載清單請看 `skills/SKILLS_MANIFEST.md`。

## 本次有查看的網頁與來源

這次除了重新搜尋，也有回頭查看前一份 `SKILL_SOURCES.md` 中列出的網頁與清單來源：

| 來源 | URL | 本次觀察 |
|---|---|---|
| Awesome Frontend Agent Skills | https://github.com/finfin/awesome-frontend-skills | 前端專用清單；適合查 React / Tailwind / React Router / TypeScript，但這份文件偏前端，通用 workflow 類 skill 較少。 |
| Awesome Claude Skills | https://github.com/travisvn/awesome-claude-skills | 綜合型 Claude Skills 索引；有官方 skills、文件處理、設計、開發、測試等分類。 |
| Awesome Claude Skills Directory | https://awesomeclaudeskills.com/ | 以 GitHub stars / trending 排序的 Claude skills 目錄；顯示 Superpowers、Anthropic Official Skills、Scientific Skills、Claude Cookbooks 等熱門項目。 |
| Superpowers on Awesome Claude Skills | https://awesomeclaudeskills.com/skill/obra/superpowers | 標示 `obra/superpowers` 為 featured，描述為 20+ battle-tested skills 的核心技能庫。 |
| Claude 官方 Superpowers Plugin | https://claude.com/plugins/superpowers | 官方 plugin 頁面描述 Superpowers 會教 Claude brainstorming、subagent development with code review、debugging、TDD、skill authoring。 |
| SkillsMP | https://skillsmp.com/ | Marketplace，頁面標示有大量 agent skills；熱門片段中看到 `brainstorming.md` 來自 `obra/superpowers`，以及 `vercel-react-best-practices.md`。 |
| Claude Skills Library | https://claudeskills.club/ | Marketplace / directory；分類數量包含 Developer Tools、Code Generation、Architecture Design、Testing and QA、Code Review、Project Management、Debugging 等。 |
| LobeHub Skills | https://lobehub.com/skills | Marketplace；可查 Claude / Codex / ChatGPT SKILL.md。頁面片段顯示 `webapp-testing` 等官方 / GitHub skills。 |
| MCPMarket Skills | https://mcpmarket.com/tools/skills | 本次請求時遇到 429 Too Many Requests；之後可再查 leaderboard。 |
| SkillsMD | https://skillsmd.dev/ | Open Agent Skills Registry；主打 browse / install / share reusable skills，並依 usage 排名。 |
| Skill Leaderboard | https://www.skillleaderboard.com/ | 以 GitHub data signals 排名 agent skills；可用來追蹤最快成長或大量使用的 skill。 |
| SkillRegistry | https://skillregistry.io/ | AI skills / agent tools directory；頁面片段中可看到 `skill-creator`、`agent-browser` 等項目。 |
| Skills Playground | https://skillsplayground.com/ | Claude Code marketplace / MCP server list；頁面片段中可看到 `Using Superpowers`、`Requesting Code Review` 等在熱門列表中。 |
| AgenticSkills | https://agenticskills.io/ | Agent skills + MCP directory；頁面片段中可看到 `Using Superpowers`、`Skill Creator` 等高評級 / 高使用量項目。 |
| Firecrawl Blog: Best Claude Code Skills | https://www.firecrawl.dev/blog/best-claude-code-skills | 推薦 Firecrawl、Karpathy guidelines、Frontend Design、Superpowers、Vercel Web Design Guidelines、Vercel React Best Practices、Document Skills、Webapp Testing、Trail of Bits Security、Skill Creator 等。 |
| OpenAIToolsHub best skills article | https://openaitoolshub.org/en/blog/best-claude-code-skills-2026 | 文章自稱整理 349 個 Claude Code skills；片段指出最省時間的包含 `superpowers/test-driven-development`、`superpowers/systematic-debugging`、`code-reviewer`、`superpowers/brainstorming`、`frontend-design`。 |
| Agensi best Claude Code skills article | https://www.agensi.io/learn/best-claude-code-skills-2026 | 測試型推薦文，聚焦 code review、testing、frontend design、DevOps 等高價值技能。 |
| Better Stack Superpowers Framework | https://betterstack.com/community/guides/ai/superpowers-framework/ | Superpowers methodology 解說，適合了解為什麼它偏向完整開發流程，而不是單一 prompt。 |

## 最優先推薦：Superpowers

| 項目 | 內容 |
|---|---|
| Repository | https://github.com/obra/superpowers |
| 官方 plugin | https://claude.com/plugins/superpowers |
| 定位 | 通用軟體開發方法論 + composable skills；適合規範 AI coding agent 的整套工作流程。 |
| 適用 agent | Claude Code、Codex CLI、Codex App、Factory Droid、Gemini CLI、OpenCode、Cursor、GitHub Copilot CLI 等。 |
| 為什麼推薦 | 它不是只有單一 prompt，而是覆蓋 brainstorming、spec、plan、TDD、debugging、subagent、code review、verification、git worktree、skill authoring 的完整流程。 |
| 使用情境 | 做新功能、修 bug、拆需求、寫計畫、讓 subagent 分工、要求測試先行、做 code review、收尾前驗證。 |

### Superpowers 主要 skills

以下是本次直接查看 `obra/superpowers` repo 的 `skills/` 目錄與 raw `SKILL.md` frontmatter 後整理：

| Skill | 作用 |
|---|---|
| `using-superpowers` | 對話開始時建立「先找技能、再回應」的工作規則。 |
| `brainstorming` | 實作前先探索意圖、需求、設計；適合任何創作、功能、元件或行為變更。 |
| `writing-plans` | 已有 spec 或需求後，先寫可執行的實作計畫，再碰程式碼。 |
| `executing-plans` | 依已寫好的實作計畫執行，並設 review checkpoints。 |
| `subagent-driven-development` | 將 implementation plan 拆成獨立任務，交給 subagent 平行或分段執行。 |
| `dispatching-parallel-agents` | 有 2 個以上互不相依任務時，平行派發 agent。 |
| `test-driven-development` | 實作任何 feature / bugfix 前先做 TDD。 |
| `systematic-debugging` | 遇到 bug、測試失敗、非預期行為時，先做根因分析，不直接猜修法。 |
| `requesting-code-review` | 完成任務、重大 feature 或 merge 前要求 code review。 |
| `receiving-code-review` | 收到 review feedback 時，先理解與驗證，不盲目接受。 |
| `verification-before-completion` | 宣稱完成、修好、測試通過前，必須先執行驗證命令並確認輸出。 |
| `finishing-a-development-branch` | 實作完成且測試通過後，決定 merge、PR 或 cleanup 的收尾流程。 |
| `using-git-worktrees` | 開始隔離 feature work 或執行計畫前，用 git worktree / workspace 隔離。 |
| `writing-skills` | 建立、編輯、驗證 skills。 |

### Superpowers 建議之後使用方式

如果之後只想先學一套通用 workflow，建議優先研究這個順序：

1. `using-superpowers`
2. `brainstorming`
3. `writing-plans`
4. `test-driven-development`
5. `systematic-debugging`
6. `subagent-driven-development`
7. `requesting-code-review`
8. `verification-before-completion`

## Anthropic 官方 Skills

| 項目 | 內容 |
|---|---|
| Repository | https://github.com/anthropics/skills |
| 定位 | 官方 Agent Skills 範例、規格、template 與常用能力。 |
| 為什麼推薦 | 官方來源，品質與格式最值得參考；也適合學習 skill 設計。 |

### 值得優先研究的官方 skills

| Skill | 推薦原因 |
|---|---|
| `skill-creator` | 建立、修改、優化 skills；之後本專案要整理 AG Grid / Antd / i18n / form skill 時很有用。 |
| `webapp-testing` | 用 Playwright 測 local web app，可驗證前端功能、console、UI、browser logs。 |
| `frontend-design` | 建立更有設計感、非 AI 預設感的前端介面。 |
| `web-artifacts-builder` | React、Tailwind、shadcn/ui 等複雜 HTML artifacts 建構流程。 |
| `docx` / `pdf` / `pptx` / `xlsx` | 文件處理通用技能，非前端但在日常工作很實用。 |
| `mcp-builder` | 建立 MCP server 的通用技能，若之後要把前端資料源或工具變成 MCP 可用。 |
| `claude-api` | 建立、debug、優化 Anthropic SDK / Claude API app。 |
| `theme-factory` | 替文件、簡報、HTML landing page 等套用一致主題。 |

## Addy Osmani / agent-skills

| 項目 | 內容 |
|---|---|
| Repository | https://github.com/addyosmani/agent-skills |
| 定位 | Production-grade engineering skills for AI coding agents。 |
| 為什麼推薦 | 很適合補強「工程流程」：spec、planning、TDD、review、debugging、security、performance、documentation。 |

### 值得優先研究的 skills

| Skill | 作用 |
|---|---|
| `using-agent-skills` | Meta-skill：開始 session 或需要判斷該用哪個 skill 時使用。 |
| `spec-driven-development` | 新專案、新功能或重大變更前先產出 spec。 |
| `planning-and-task-breakdown` | 把大任務拆成可執行任務，評估 scope 與可平行工作項目。 |
| `test-driven-development` | 實作邏輯、修 bug、改行為時以測試驅動。 |
| `incremental-implementation` | 避免一次大量修改；多檔案變更時拆小步交付。 |
| `source-driven-development` | 依官方文件做 implementation decision，減少過時或幻覺寫法。 |
| `debugging-and-error-recovery` | 系統化根因 debugging。 |
| `code-review-and-quality` | merge 前多維度 code review。 |
| `security-and-hardening` | 處理 user input、auth、data storage、third-party service 時強化安全。 |
| `performance-optimization` | 效能需求、Core Web Vitals、load time 或 profiling bottleneck 時使用。 |
| `documentation-and-adrs` | 建築決策、API 變更、功能交付時紀錄 ADR / docs。 |
| `git-workflow-and-versioning` | commit、branch、conflict、parallel streams 的 git 工作流。 |
| `context-engineering` | 新 session、切換任務、agent 輸出品質下降時整理 context。 |
| `frontend-ui-engineering` | 建構 production-quality UI；與本專案前端能力目標高度相關。 |
| `browser-testing-with-devtools` | 需要真瀏覽器 DOM、console、network、performance、visual 驗證時使用。 |

## Vercel Agent Skills

| 項目 | 內容 |
|---|---|
| Repository | https://github.com/vercel-labs/agent-skills |
| 定位 | Vercel 官方 agent skills。 |
| 為什麼推薦 | 對 React / Next.js / web design / performance / deployment 有高實用性；雖然本專案不一定用 Next.js，React 與 UI guideline 仍可參考。 |

### 值得優先研究的 skills

| Skill | 作用 |
|---|---|
| `vercel-react-best-practices` | React / Next.js performance optimization；寫、review、refactor React code 時使用。 |
| `web-design-guidelines` | UI / UX / accessibility / design audit。 |
| `vercel-composition-patterns` | 可擴充 React composition patterns。 |
| `vercel-react-view-transitions` | React View Transition API 動畫與 route transition。 |
| `vercel-optimize` | Vercel 成本與效能優化。 |
| `deploy-to-vercel` | Deploy app / website 到 Vercel。 |
| `vercel-cli-with-tokens` | 使用 token-based auth 操作 Vercel CLI。 |

## Trail of Bits Security Skills

| 項目 | 內容 |
|---|---|
| Repository | https://github.com/trailofbits/skills |
| 定位 | Trail of Bits Claude Code plugin marketplace；安全分析、測試、審計流程。 |
| 為什麼推薦 | 若之後要讓 AI 檢查前端 supply chain、CI、GitHub Actions、API integration、C/C++ 或 smart contract 安全，可作為高品質安全 skill 來源。 |

### README 中看到的 plugin / skill 方向

- `building-secure-contracts`
- `entry-point-analyzer`
- `agentic-actions-auditor`
- `audit-context-building`
- `c-review`
- `differential-review`
- `dimensional-analysis`
- `fp-check`
- `insecure-defaults`
- `semgrep-rule-creator`
- `semgrep-rule-variant-creator`

## Firecrawl / Web Data Skills

| 項目 | 內容 |
|---|---|
| Repository | https://github.com/firecrawl/firecrawl-claude-plugin |
| CLI / Skill | https://github.com/firecrawl/cli |
| 官方 plugin | https://claude.com/plugins/firecrawl |
| 產品頁 | https://www.firecrawl.dev/skills |
| 定位 | 給 agent 使用 web scraping / crawling / extraction 的能力。 |
| 為什麼推薦 | 之後如果要大量從網站、文件、blog、registry 蒐集 skill 或前端最佳實務，Firecrawl 類能力很有用。 |

## 其他值得追蹤的通用 Skill Collections

| Repository / 網站 | 推薦原因 |
|---|---|
| https://github.com/Jeffallan/claude-skills | Full-stack developer skills；包含 `react-expert`、`typescript-pro`、`code-reviewer`、`debugging-wizard`、`playwright-expert` 等。 |
| https://github.com/softaworks/agent-toolkit | 多種通用 agent toolkit；包含 `react-dev`、`react-useeffect`、`openapi-to-typescript`、QA、文件、溝通與專案流程 skills。 |
| https://github.com/wshobson/agents | 大型 multi-harness agentic plugin marketplace；skills 分散在 `plugins/*/skills`，包含 UI design、frontend/mobile、TypeScript、parallel debugging、team coordination。 |
| https://github.com/bmad-labs/skills | TypeScript clean code、unit testing、E2E testing、UI/UX、RCA、multi-repo git ops 等。 |
| https://github.com/awesome-skills/code-review-skill | 專門 code review；含 React、TypeScript、CSS、architecture、performance。 |
| https://github.com/millionco/react-doctor | React 專案品質 / 效能 / 安全 / 架構診斷；偏前端但可作為通用 QA 流程的一部分。 |
| https://github.com/heilcheng/awesome-agent-skills | Agent Skill Index；強調 real-world skills 與多 agent 相容性。 |
| https://github.com/karanb192/awesome-claude-skills | 50+ Claude agent skills curated list，分類包含 testing、debugging、workflow、architecture、security、documentation、meta skills。 |
| https://github.com/obviousworks/Claude-AI-skills-collection-2026 | Claude Skills collection，偏彙整官方與社群 skill。 |
| https://github.com/multica-ai/andrej-karpathy-skills | 不是標準 SKILL.md collection，而是 Karpathy-style CLAUDE.md / coding guidelines；可作為 coding style / agent behavior 參考。 |

## 建議的「通用 Skill 套件」優先級

### A. 最小核心組合

若只選一組通用 workflow，建議：

1. `obra/superpowers`
   - `using-superpowers`
   - `brainstorming`
   - `writing-plans`
   - `test-driven-development`
   - `systematic-debugging`
   - `requesting-code-review`
   - `verification-before-completion`
2. `anthropics/skills`
   - `skill-creator`
   - `webapp-testing`
   - `frontend-design`
3. `addyosmani/agent-skills`
   - `source-driven-development`
   - `incremental-implementation`
   - `code-review-and-quality`
   - `security-and-hardening`
   - `performance-optimization`

### B. 前端 AI 能力補強組合

本專案目標是提升 AI 寫前端的能力，因此通用 skill 之外，建議一起研究：

1. `anthropics/skills/frontend-design`
2. `anthropics/skills/webapp-testing`
3. `addyosmani/agent-skills/frontend-ui-engineering`
4. `addyosmani/agent-skills/browser-testing-with-devtools`
5. `vercel-labs/agent-skills/vercel-react-best-practices`
6. `vercel-labs/agent-skills/web-design-guidelines`
7. `vercel-labs/agent-skills/vercel-composition-patterns`
8. `wshobson/agents` 的 UI / frontend / Tailwind / React state management skills

### C. 品質與安全組合

1. `superpowers/test-driven-development`
2. `superpowers/systematic-debugging`
3. `superpowers/requesting-code-review`
4. `addyosmani/agent-skills/code-review-and-quality`
5. `addyosmani/agent-skills/security-and-hardening`
6. `trailofbits/skills`
7. `awesome-skills/code-review-skill`

### D. 蒐集資料與建立自有 Skill 組合

1. `anthropics/skills/skill-creator`
2. `superpowers/writing-skills`
3. `addyosmani/agent-skills/source-driven-development`
4. Firecrawl plugin / CLI
5. Skills registry / leaderboard：SkillsMP、SkillsMD、SkillLeaderboard、SkillRegistry、AgenticSkills、Skills Playground

## 已下載到 `skills/` staging 的通用核心集合

2026-05-28 已下載 59 個可移植 skill 目錄，其中通用 workflow 重點包含：

- Superpowers：`using-superpowers`、`brainstorming`、`writing-plans`、`executing-plans`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion` 等 14 個。
- Anthropic 官方：`skill-creator`、`frontend-design`、`webapp-testing`、`web-artifacts-builder`。
- Addy Osmani engineering workflow：`using-agent-skills`、`spec-driven-development`、`planning-and-task-breakdown`、`source-driven-development`、`incremental-implementation`、`code-review-and-quality`、`security-and-hardening`、`performance-optimization`、`frontend-ui-engineering`、`browser-testing-with-devtools` 等。
- 前端與品質補強：Vercel、Softaworks、wshobson、React Router、Ant Design、secondsky、Playwright、AG Grid、code review skills。

完整來源、commit 與原始路徑請看 `skills/SKILLS_MANIFEST.md`；驗證結果請看 `skills/VALIDATION_REPORT.md`。

## 後續搜尋關鍵字

```text
superpowers Claude Code skills
obra superpowers SKILL.md
best Claude Code skills 2026
most popular agent skills SKILL.md
agent skills leaderboard
Claude skills marketplace popular
Claude Code skills TDD debugging code review
SKILL.md test-driven-development systematic-debugging code-review
Anthropic official skills skill-creator webapp-testing
Vercel agent skills react best practices web design guidelines
Trail of Bits Claude skills security
Firecrawl Claude Code skill
```

## 注意事項

1. 有些網站的數字可能是 marketplace 自己計算的 installs / views / GitHub signals，不一定等於真實使用量。
2. GitHub stars 可以作為初步參考，但仍要讀 `SKILL.md` 內容，確認是否符合本專案需要。
3. 有些熱門資源是 `CLAUDE.md`、prompt、plugin、MCP server，不一定是標準 `SKILL.md`，需要分開紀錄。
4. 之後如果要實際下載，建議先建立 `downloads/` 或 `external/` 目錄，並紀錄來源、授權、下載日期與 commit SHA。
5. 對本專案最有價值的不是「下載最多 skill」，而是整理出能穩定提升前端品質的工作流程：設計 → 計畫 → TDD → 實作 → 瀏覽器驗證 → code review → 完成前驗證。
