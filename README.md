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

## 文件

- [Skill 來源清單](./SKILL_SOURCES.md)：紀錄常見可下載 skill 的網站、GitHub repositories、安裝指令與後續搜尋關鍵字。
- [通用 Skill 調查紀錄](./UNIVERSAL_SKILLS_RESEARCH.md)：紀錄推薦、大量使用或值得優先研究的通用 skills，例如 Superpowers、Anthropic 官方 skills、Addy Osmani engineering skills、Vercel skills 等。
- [前端專用 Skill 調查紀錄](./FRONTEND_SPECIALIZED_SKILLS_RESEARCH.md)：紀錄 React、TypeScript、Tailwind、AG Grid、Ant Design、i18n、React Router、React Hook Form 等專用 skills。
- [AI Coding Agent Skill 放置方式調查](./AGENT_SKILL_LAYOUTS_RESEARCH.md)：紀錄 Claude Code、OpenCode、Kilo Code、Codex、Cline、Cursor 等工具的 skills / rules / commands / agents 目錄放置方式，並規劃之後的 `skills/` staging 結構。
