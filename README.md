# frontend-skill

## 專案目的

這個專案的目的是為了收集網路上好用的 skill。蒐集這些 skill 是為了提升 AI 撰寫前端的能力。

## 前端專案技術棧

前端專案使用下列內容：

1. React
2. TypeScript
3. Tailwind
4. AG Grid React
5. Ant Design (Antd)
6. react-i18next
7. react-router-dom
8. react-hook-form

## 已下載的 skills

已將推薦 skills 安裝到專案層級 staging 目錄：

- [`skills/`](./skills/)：可移植 skill 目錄；每個可安裝 skill 位於 `skills/<skill-name>/SKILL.md`。
- [`skills/SKILLS_MANIFEST.md`](./skills/SKILLS_MANIFEST.md)：紀錄已下載 skill、來源 repository、commit、原始路徑與用途。
- [`skills/VALIDATION_REPORT.md`](./skills/VALIDATION_REPORT.md)：紀錄 frontmatter、安全掃描與 false positive 檢查結果。

移植到不同 AI coding agent 時，將需要的 `skills/<skill-name>/` 複製到該 agent 的父目錄即可，例如 `.claude/skills/<skill-name>/` 或 `.opencode/skills/<skill-name>/`。

新增重點：`skills/typescript-code-reviewer/` 是本專案整理的 TypeScript / TSX 專用 code reviewer skill，用於 review `any`/`unknown`、unsafe assertions、strict tsconfig、async/error handling、React hooks、XSS 與測試覆蓋。

新增重點：`skills/audit-code-reviewer/` 是 MIT 授權的平行多 reviewer audit skill，適合 merge / release 前讓多個 sub-agent 分別檢查 correctness、tests、security、architecture、frontend runtime 與文件/operability。

新增重點：`skills/secpriv-code-review/` 是 Meta / Facebook Research 的 MIT 授權 SecPriv security + privacy review skill，本專案加上相容 frontmatter 後放入 staging，用於 CWE/GDPR 對應、detector-validator 與高信心 findings。

新增重點：`skills/frontend-staged-review-workflow/` 是本專案整理的前端 staged diff review workflow；只 review `git add` 後的 `git diff --cached`，每個選用 review skill 至少派 2 個 sub-agent，並明確排除 unit test 建議。

新增重點：`skills/frontend-staged-commit-message/` 是本專案整理的前端 staged commit message skill；只讀 `git diff --cached`，不 stage、不 commit、不改檔，輸出 `feat: ...` / `fix: ...` / `style: ...` 這類不含 scope 括號的單行英文 commit message。

新增重點：`skills/frontend-debug-workflow/` 是本專案整理的前端 debug workflow；使用者提供程式碼位置與問題後，先讀指定檔案與附近使用、建立 evidence / root cause，再選 exact local frontend skills 修正並驗證。

新增重點：`skills/playwright-mcp-usage/` 是使用者提供的 Playwright MCP 使用流程；當一般網路搜尋被阻擋時，用真實瀏覽器 session 進行 DOM 讀取、截圖檢查與受控互動。

## 文件

- [Skill 來源清單](./SKILL_SOURCES.md)：紀錄常見可下載 skill 的網站、GitHub repositories、安裝指令與後續搜尋關鍵字。
- [通用 Skill 調查紀錄](./UNIVERSAL_SKILLS_RESEARCH.md)：紀錄推薦、大量使用或值得優先研究的通用 skills，例如 Superpowers、Anthropic 官方 skills、Addy Osmani engineering skills、Vercel skills 等。
- [前端專用 Skill 調查紀錄](./FRONTEND_SPECIALIZED_SKILLS_RESEARCH.md)：紀錄 React、TypeScript、Tailwind、AG Grid、Ant Design、i18n、React Router、React Hook Form 等專用 skills。
- [AI Coding Agent Skill 放置方式調查](./AGENT_SKILL_LAYOUTS_RESEARCH.md)：紀錄 Claude Code、OpenCode、Kilo Code、Codex、Cline、Cursor 等工具的 skills / rules / commands / agents 目錄放置方式，並規劃之後的 `skills/` staging 結構。
- [前端任務前期 Workflow 調查與草案](./FRONTEND_TASK_PREFLIGHT_WORKFLOW.md)：整理使用者目標、相關程式碼、Figma/設計稿落差、sub-agent 分工、網路 research、implementation plan 與 plan review 的前期工作流，之後可轉成 skill。
- [Code Review Skills 調查與安裝紀錄](./CODE_REVIEW_SKILLS_RESEARCH.md)：盤點現有 review/quality skills，並記錄本次新增的 `audit-code-reviewer` 與 `secpriv-code-review`。
- [`frontend-staged-review-workflow` research notes](./skills/frontend-staged-review-workflow/references/research-notes.md)：記錄前端 staged review workflow 的外部來源與設計決策。
- [前端 Debug Workflow](./FRONTEND_DEBUG_WORKFLOW.md)：整理「使用者給程式碼位置 + 問題 → 查附近使用 → root cause → 選 skill → 修正 → 驗證 → 紀錄」的 debug 工作流。
- [`frontend-debug-workflow` research notes](./skills/frontend-debug-workflow/references/research-notes.md)：記錄前端 debug workflow 的外部來源與設計決策。
