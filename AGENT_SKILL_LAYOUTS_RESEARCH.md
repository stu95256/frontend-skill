# AI Coding Agent 的 Skill / Rules / Commands 放置方式調查

最後調查日期：2026-05-28

## 目的

我們已經整理了大量可用的前端與通用 skills，並在 2026-05-28 將推薦的核心集合下載到本專案的 `skills/` staging 目錄。本文件保留各 AI coding agent runtime 目錄的放置規劃，方便之後把 `skills/<skill-name>/` 複製到 `.claude/skills/`、`.opencode/skills/`、`.agents/skills/` 或 `.kilo/skills/`。

本文件重點是回答：如果之後要把同一批 skill 分別給 Kilo Code、Claude Code、OpenCode、Codex CLI、Cline / Cursor 等 AI coding agent 使用，各工具的 skill、rules、commands、agents 目錄應該如何放置？

## 核心結論

不同 agent 對「skill」的支援程度不一樣，但目前最值得採用的共同格式是：

```text
<skill-name>/
└── SKILL.md
```

也就是 Agent Skills open standard 的資料夾格式。`SKILL.md` 通常包含 YAML frontmatter，例如 `name`、`description`，以及正文的操作步驟、規範、範例、引用檔案說明。

最重要的相容性結論：

1. Claude Code 原生讀取：`.claude/skills/<skill-name>/SKILL.md`
2. OpenCode 原生讀取：`.opencode/skills/<skill-name>/SKILL.md`
3. OpenCode 也讀取相容目錄：`.claude/skills/<skill-name>/SKILL.md`、`.agents/skills/<skill-name>/SKILL.md`
4. Kilo Code 新平台原生讀取：`.kilo/skills/<skill-name>/SKILL.md`
5. Kilo Code 也讀取相容目錄：`.agents/skills/<skill-name>/SKILL.md`、`.claude/skills/<skill-name>/SKILL.md`
6. Codex 原生讀取：`.agents/skills/<skill-name>/SKILL.md`
7. 因此若要一份 skill 給多工具共用，`.agents/skills/` 是很好的跨工具 runtime 目錄，但 Claude Code 仍需要 `.claude/skills/`。
8. 本專案根目錄的 `skills/` 比較適合作為「下載與整理用 staging / catalog」，不要假設所有 agent 都會自動讀取根目錄 `skills/`。

建議未來採用「兩層結構」：

```text
frontend-skill/
├── skills/                         # 我們自己的 canonical staging：下載、審核、分類、保留來源
│   ├── SKILLS_MANIFEST.md          # 已下載 skill 的來源、commit、原始路徑、用途
│   ├── VALIDATION_REPORT.md        # frontmatter / secret / dangerous command 掃描結果
│   ├── <skill-name>/SKILL.md       # 可直接移植到各 agent runtime 的 flat skill 目錄
│   └── ...
│
├── .agents/skills/                 # runtime：Codex / OpenCode / Kilo 可讀
│   └── <skill-name>/SKILL.md
│
├── .claude/skills/                 # runtime：Claude Code 必要；OpenCode / Kilo 也可相容讀取
│   └── <skill-name>/SKILL.md
│
├── .opencode/skills/               # runtime：只有需要 OpenCode 專用覆寫時才放
│   └── <skill-name>/SKILL.md
│
└── .kilo/skills/                   # runtime：只有需要 Kilo 專用覆寫時才放
    └── <skill-name>/SKILL.md
```

在 Windows 環境下，symlink 可能受權限或 Developer Mode 影響。未來若要自動同步 runtime 目錄，建議先用「複製腳本」而不是 symlink；等確認權限與工具行為後，再考慮 junction / symlink。

## 術語區分

### Skill

可重複使用的能力包，通常是：

```text
<skill-name>/SKILL.md
```

適合放：React 元件設計流程、TypeScript 重構流程、Tailwind / shadcn UI 規範、AG Grid debug 流程、Ant Design form pattern、i18n 檢查流程、Playwright 測試流程等。

### Rules / Instructions

持久性專案規則。通常會在每次 agent 啟動時被讀入，不一定是 on-demand。

適合放：專案 coding style、命令、禁止事項、架構規則、測試要求、安全規範。

典型檔案：

- `AGENTS.md`
- `CLAUDE.md`
- `.clinerules/`
- `.cursor/rules/*.mdc`
- `.kilo/rules/*.md`

### Commands

手動叫用的 slash command 或快捷流程。Claude Code 舊式 commands 是 `.claude/commands/*.md`，但 Claude Code 官方文件已說 custom commands 已經合併到 skills，建議新流程優先用 `.claude/skills/<name>/SKILL.md`。

### Agents / Subagents

專門化 agent 設定，通常是 Markdown + YAML frontmatter 或 JSON config。適合「code reviewer」、「docs writer」、「security auditor」這類角色，不等同於 skill。

## 各工具放置方式總覽

| 工具 | Skill 主要位置 | 跨工具相容位置 | Rules / instructions | Commands / agents |
|---|---|---|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md`、`~/.claude/skills/<name>/SKILL.md` | Claude 文件未明列 `.agents/skills` | `CLAUDE.md` 等 Claude memory / settings | `.claude/commands/*.md` 仍可用，但新建議用 skills；plugin 可有 `skills/` |
| OpenCode | `.opencode/skills/<name>/SKILL.md`、`~/.config/opencode/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md`、`.agents/skills/<name>/SKILL.md` | `AGENTS.md`；也可用 `opencode.json` instructions | `.opencode/agents/*.md`、`~/.config/opencode/agents/*.md` |
| Kilo Code | `.kilo/skills/<name>/SKILL.md`、`~/.kilo/skills/<name>/SKILL.md` | `.agents/skills/`、`.claude/skills/`；舊平台 `.kilocode/skills/` | `AGENTS.md`、`kilo.jsonc` 的 `instructions`、`.kilo/rules/*.md`、舊 `.kilocode/rules/` | `.kilo/agents/*.md`、`.kilo/agent/*.md`、`kilo.jsonc` 的 `agent` |
| Codex CLI | `.agents/skills/<name>/SKILL.md`、`$HOME/.agents/skills/<name>/SKILL.md` | 主要就是 open agent standard `.agents/skills` | `AGENTS.md`，全域 `~/.codex/AGENTS.md` | Codex subagents / plugins 另有設定；skills 可用 `$skill-installer` |
| Cline | 官方 rules 主要是 `.clinerules/` | 可偵測 `AGENTS.md`、`.cursorrules`、`.windsurfrules` | `.clinerules/*.md`、global Cline Rules | Cline docs 另有 Skills / Plugins，但本輪只確認 rules 位置 |
| Cursor | `.cursor/rules/*.mdc` | 不以 Agent Skills 為主 | project rules / user rules | 無通用 `SKILL.md` runtime 目錄可依賴 |

## Claude Code

來源：

- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/plugins-reference

### Skill 目錄

Claude Code skill 是一個資料夾，入口檔為 `SKILL.md`：

```text
my-skill/
├── SKILL.md           # 必要
├── template.md        # 可選
├── examples/
│   └── sample.md      # 可選
└── scripts/
    └── validate.sh    # 可選
```

可放置位置：

```text
~/.claude/skills/<skill-name>/SKILL.md       # personal，所有專案可用
.claude/skills/<skill-name>/SKILL.md         # project，僅目前專案可用
<plugin>/skills/<skill-name>/SKILL.md        # plugin 內的 skill
```

Claude Code 會從啟動目錄往上到 repo root 尋找 `.claude/skills/`，也支援在子目錄工作時按需發現 nested `.claude/skills/`。

### Command 名稱

Claude Code 的 slash command 名稱來自目錄或檔名：

```text
.claude/skills/deploy-staging/SKILL.md  -> /deploy-staging
.claude/commands/deploy.md              -> /deploy
my-plugin/skills/review/SKILL.md        -> /my-plugin:review
```

注意：`SKILL.md` frontmatter 的 `name` 通常只是顯示名稱，不改變 `/skill-name`。命令名稱主要取自 skill 目錄名稱。

### Commands 與 skills 的關係

Claude Code 文件指出 custom commands 已經合併到 skills：

```text
.claude/commands/deploy.md
.claude/skills/deploy/SKILL.md
```

兩者都可以產生 `/deploy`，但 skills 支援 supporting files、frontmatter、automatic invocation 等能力。因此未來新整理的技能應優先使用 `.claude/skills/<name>/SKILL.md`。

### 對本專案的意義

如果要支援 Claude Code，不能只放 `.agents/skills/`。至少要把選定 skill 複製或同步到：

```text
.claude/skills/<skill-name>/SKILL.md
```

## OpenCode

來源：

- https://opencode.ai/docs/skills/
- https://opencode.ai/docs/rules/
- https://opencode.ai/docs/agents/

### Skill 目錄

OpenCode 的 skill 同樣使用 `SKILL.md` 資料夾格式。官方列出的搜尋位置：

```text
.opencode/skills/<name>/SKILL.md             # project config
~/.config/opencode/skills/<name>/SKILL.md    # global config
.claude/skills/<name>/SKILL.md               # project Claude-compatible
~/.claude/skills/<name>/SKILL.md             # global Claude-compatible
.agents/skills/<name>/SKILL.md               # project agent-compatible
~/.agents/skills/<name>/SKILL.md             # global agent-compatible
```

OpenCode 對 project-local path 會從目前工作目錄往上走到 git worktree，載入沿途的 `.opencode/skills/*/SKILL.md`、`.claude/skills/*/SKILL.md`、`.agents/skills/*/SKILL.md`。

### Skill frontmatter

OpenCode 要求 `SKILL.md` 開頭有 YAML frontmatter，至少重視：

```yaml
---
name: react-component-patterns
description: Use when creating or refactoring React components in this project.
---
```

官方列出可辨識欄位包含：

- `name`，required
- `description`，required
- `license`，optional
- `compatibility`，optional
- `metadata`，optional string-to-string map

### Rules

OpenCode 主要用 `AGENTS.md` 作為 project instructions。可用 `/init` 產生或更新 `AGENTS.md`。官方建議將專案的 `AGENTS.md` commit 到 Git。

適合放入 `AGENTS.md` 的內容：

- build / lint / test commands
- 命令執行順序
- 架構與檔案導覽規則
- 專案慣例
- 驗證步驟

### Agents

OpenCode 可用 JSON 或 Markdown 定義 agents：

```text
.opencode/agents/<agent-name>.md             # project
~/.config/opencode/agents/<agent-name>.md    # global
```

Markdown 檔名會成為 agent 名稱。frontmatter 可放 `description`、`mode`、`model`、`temperature`、`permission` 等；正文是 agent 的 system prompt。

### 對本專案的意義

若我們將選定 skill 同步到 `.agents/skills/`，OpenCode 可以讀取；若要 OpenCode 專用版本，再放 `.opencode/skills/`。

## Kilo Code

來源：

- https://kilo.ai/docs/llms.txt
- Kilo docs `/customize/skills`
- Kilo docs `/customize/agents-md`
- Kilo docs `/customize/custom-rules`
- Kilo docs `/customize/custom-subagents`
- https://kilo.ai/docs/customize/custom-rules
- https://kilo.ai/docs/customize/custom-modes

### Skill 目錄：新平台

Kilo Code 實作 Agent Skills open format。skill 是資料夾 + `SKILL.md`。

新平台的主要位置：

```text
~/.kilo/skills/<skill-name>/SKILL.md       # global/user
.kilo/skills/<skill-name>/SKILL.md         # project/workspace
```

Kilo 也支援跨工具相容目錄：

```text
.agents/skills/<skill-name>/SKILL.md       # open agent standard，預設載入
.claude/skills/<skill-name>/SKILL.md       # Claude Code compatibility；VSCode 文件說需啟用 compatibility，CLI 文件列為相容讀取
```

也可在 `kilo.jsonc` 設定額外 skill path 或遠端 URL：

```jsonc
{
  "skills": {
    "paths": ["/path/to/shared/skills", "~/my-skills", "relative/skills"],
    "urls": ["https://example.com/skills/my-skill/SKILL.md"]
  }
}
```

`skills.paths` 可接受絕對路徑、`~/` home-relative path、或相對 project root 的路徑。

### Skill 目錄：舊 VS Code platform

舊平台使用 `.kilocode`：

```text
~/.kilocode/skills/<skill-name>/SKILL.md       # global generic
.kilocode/skills/<skill-name>/SKILL.md         # project generic
.kilocode/skills-code/<skill-name>/SKILL.md    # project code mode only
```

舊平台支援 mode-specific skill 目錄：

```text
.kilocode/skills-code/<skill-name>/SKILL.md
.kilocode/skills-architect/<skill-name>/SKILL.md
.kilocode/skills-ask/<skill-name>/SKILL.md
.kilocode/skills-debug/<skill-name>/SKILL.md
```

新平台不使用 mode-specific skill directories，而是把 skills 放在 shared pool，讓 agent 根據 `description` 決定何時使用。

### Rules / instructions

Kilo 新平台 project rules 主要透過 `kilo.jsonc` 的 `instructions` 指向檔案或 glob：

```jsonc
{
  "instructions": [".kilo/rules/formatting.md", ".kilo/rules/*.md"]
}
```

建議目錄：

```text
.kilo/rules/formatting.md
.kilo/rules/restricted-files.md
.kilo/rules/naming-conventions.md
```

global rules 通常在 global `kilo.jsonc`，位置約為：

```text
~/.config/kilo/kilo.jsonc
```

舊平台相容：

```text
.kilocode/rules/*.md
~/.kilocode/rules/*.md
.kilocode/rules-code/*.md
.kilocode/rules-debug/*.md
.kilocode/rules-ask/*.md
```

Kilo legacy fallback files：

```text
.roorules
.clinerules
.kilocoderules    # deprecated
```

### AGENTS.md

Kilo Code 會自動載入 `AGENTS.md`。建議放在 project root：

```text
AGENTS.md
```

也支援 fallback：

```text
AGENT.md
```

注意大小寫：文件強調要用 uppercase `AGENTS.md`，不是 `agents.md`。

Kilo 支援 subdirectory AGENTS.md：

```text
frontend-skill/
├── AGENTS.md
├── src/
│   └── AGENTS.md
└── docs/
    └── AGENTS.md
```

子目錄規則會對該子目錄工作更具體，衝突時可覆蓋上層。

### Custom agents / subagents

Kilo 新平台可用 Markdown agents：

```text
.kilo/agents/<agent-name>.md
.kilo/agent/<agent-name>.md
.opencode/agents/<agent-name>.md
~/.config/kilo/agent/<agent-name>.md
```

Custom subagents 文件也列出：

```text
.kilo/agents/<agent-name>.md                 # project-specific
~/.config/kilo/agents/<agent-name>.md        # global
```

也可在 project `kilo.jsonc` 的 `agent` 區塊設定：

```jsonc
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "mode": "subagent",
      "prompt": "{file:./prompts/code-review.txt}",
      "permission": {
        "edit": "deny",
        "bash": "deny"
      }
    }
  }
}
```

### 對本專案的意義

如果只要 Kilo Code 使用，最官方的位置是：

```text
.kilo/skills/<skill-name>/SKILL.md
```

如果要兼顧 Kilo + OpenCode + Codex，優先放：

```text
.agents/skills/<skill-name>/SKILL.md
```

如果要兼顧 Kilo + OpenCode + Claude Code，則也要放：

```text
.claude/skills/<skill-name>/SKILL.md
```

## Codex CLI

來源：

- https://developers.openai.com/codex/skills.md
- https://developers.openai.com/codex/guides/agents-md.md
- https://developers.openai.com/codex/concepts/customization.md

### Skill 目錄

Codex 支援 Agent Skills open standard。官方列出 skill 位置：

```text
$CWD/.agents/skills
$CWD/../.agents/skills
$REPO_ROOT/.agents/skills
$HOME/.agents/skills
/etc/codex/skills
```

在 repo 中，Codex 會從目前工作目錄往上到 repo root 掃描 `.agents/skills`。如果兩個 skills 有相同 `name`，Codex 不會合併，可能都出現在 selector。

Codex 支援 symlinked skill folders，會跟隨 symlink target。

### AGENTS.md

Codex 啟動時會讀取 `AGENTS.md`。發現順序：

1. Global：`~/.codex/AGENTS.override.md` 若存在優先，否則 `~/.codex/AGENTS.md`
2. Project：從 project root 往目前工作目錄走，每層檢查 `AGENTS.override.md`、`AGENTS.md`、以及 fallback filenames
3. Merge：從 root 到 current directory 串接，越靠近目前目錄的指令越晚出現，因此可覆蓋較早指令

預設 project doc 上限是 32 KiB，可用設定調整。

### 對本專案的意義

若未來要支援 Codex，最重要的是：

```text
.agents/skills/<skill-name>/SKILL.md
AGENTS.md
```

Codex 不保證會讀 `.claude/skills/` 或 `.opencode/skills/`，所以 `.agents/skills/` 是 Codex 的主要 runtime 目錄。

## Cline

來源：

- https://docs.cline.bot/customization/cline-rules

### Rules 目錄

Cline 官方 rules 是 Markdown files。Workspace rules：

```text
.clinerules/
├── coding.md
├── testing.md
└── architecture.md
```

Cline 也會偵測其他工具的 rules：

```text
.clinerules/       # Cline primary rule format
.cursorrules       # Cursor legacy rules
.windsurfrules     # Windsurf rules
AGENTS.md          # cross-tool standard
```

### 對本專案的意義

Cline 的主要共用入口比較偏 rules / instructions，而不是 `SKILL.md` runtime 目錄。若未來要支援 Cline，建議先提供：

```text
AGENTS.md
.clinerules/*.md
```

而不是假設 Cline 會直接讀 `.agents/skills/`。

## Cursor

來源：

- https://cursor.com/docs/rules

### Rules 目錄

Cursor 官方 project rules 使用：

```text
.cursor/rules/*.mdc
```

Cursor rules 不等同於 Agent Skills。`.mdc` 常含 frontmatter，用於控制規則的套用方式。

### 對本專案的意義

若未來要支援 Cursor，應把通用專案規範轉成 `.cursor/rules/*.mdc`。前端 skill 本身可以留在 `skills/` staging 或 `.agents/skills/`，但不應假設 Cursor 原生會載入 `SKILL.md`。

## 目前 staging 設計

2026-05-28 已實際下載推薦 skills 到 `skills/`，此目錄作為 canonical staging / catalog，不直接依賴任何 agent 的自動載入規則。

### 1. Canonical staging：`skills/`

目前採用 flat 結構，方便直接複製到各 agent 的 `skills/<skill-name>/` runtime 目錄：

```text
skills/
├── SKILLS_MANIFEST.md
├── VALIDATION_REPORT.md
├── using-superpowers/SKILL.md
├── frontend-design/SKILL.md
├── vercel-react-best-practices/SKILL.md
├── react-dev/SKILL.md
├── react-router-declarative-mode/SKILL.md
├── ant-design/SKILL.md
├── react-hook-form-zod/SKILL.md
└── ...
```

`SKILLS_MANIFEST.md` 記錄每個 skill 的：

- `Skill dir`
- `Source`
- `Commit`
- `Source path`
- `Why included`

`VALIDATION_REPORT.md` 記錄 frontmatter、secret/token pattern、危險命令掃描結果。

### 2. Runtime target：`.agents/skills/`

建議作為跨工具 runtime 第一順位：

```text
.agents/skills/<skill-name>/SKILL.md
```

適用：

- Codex CLI
- OpenCode
- Kilo Code

不適用 / 不保證：

- Claude Code
- Cursor
- Cline

### 3. Runtime target：`.claude/skills/`

Claude Code 必要：

```text
.claude/skills/<skill-name>/SKILL.md
```

也可被 OpenCode、Kilo Code 當 compatibility directory 讀取。

### 4. Runtime target：`.opencode/skills/`

只有需要 OpenCode 專用調整時才放：

```text
.opencode/skills/<skill-name>/SKILL.md
```

例如 OpenCode 對 frontmatter 欄位更嚴格，或要加 OpenCode-specific permission / metadata。

### 5. Runtime target：`.kilo/skills/`

只有需要 Kilo 專用調整時才放：

```text
.kilo/skills/<skill-name>/SKILL.md
```

Kilo 也可透過 `kilo.jsonc` 的 `skills.paths` 指向 `skills/frontend` 或 `skills/universal`，但這會讓 Kilo 讀到 staging 裡所有候選 skills。若 staging 含未審核 skill，不建議直接指向整個 `skills/`。

## 最小跨工具放置策略

若未來想避免重複太多，建議採用這個最小組合：

```text
skills/                         # canonical staging，所有下載原始資料都先放這裡
.agents/skills/                 # Codex + OpenCode + Kilo runtime
.claude/skills/                 # Claude Code runtime
AGENTS.md                       # 通用 project instructions
```

這樣可覆蓋：

- Claude Code：讀 `.claude/skills/`
- OpenCode：讀 `.agents/skills/` 與 `.claude/skills/`
- Kilo Code：讀 `.agents/skills/`、`.claude/skills/`，也可讀 `.kilo/skills/`
- Codex：讀 `.agents/skills/`
- Cline：讀 `AGENTS.md` 作為 instructions
- Cursor：仍建議另轉 `.cursor/rules/*.mdc`，不要只靠 AGENTS.md

## 後續真正下載 / 安裝時的建議流程

1. 先下載到 `skills/vendor/<source>/<skill-name>/`，保留來源原貌。
2. 人工或 agent 審核 `SKILL.md`：
   - 是否含有 API key / token / secrets
   - 是否要求不安全命令
   - 是否硬編碼與本專案不符的工具鏈
   - 是否有過度寬鬆的 permissions / allowed-tools
   - 是否適合 React / TypeScript / Tailwind / AG Grid / Antd / i18n / Router / Form 技術棧
3. 將通過審核的 skill 正規化到：
   - `skills/universal/<skill-name>/SKILL.md`
   - `skills/frontend/<skill-name>/SKILL.md`
4. 更新 `skills/manifest.yaml`。
5. 依 target 複製到 runtime 目錄：
   - `.agents/skills/<skill-name>/SKILL.md`
   - `.claude/skills/<skill-name>/SKILL.md`
   - 必要時 `.opencode/skills/<skill-name>/SKILL.md`
   - 必要時 `.kilo/skills/<skill-name>/SKILL.md`
6. 啟動各 agent 驗證是否可列出 / 觸發 skill。
7. 對 rules 類內容另行轉成：
   - `AGENTS.md`
   - `.kilo/rules/*.md`
   - `.clinerules/*.md`
   - `.cursor/rules/*.mdc`

## 本專案的暫定決策

目前先不下載、不安裝。後續如果使用者開始要求下載，建議先採用：

```text
skills/                 # 下載與審核 staging
.agents/skills/         # Codex / OpenCode / Kilo runtime
.claude/skills/         # Claude Code runtime
AGENTS.md               # 跨工具專案規範
```

`skills/` 裡的候選 skill 不應自動全部暴露給 agent，避免未審核內容進入 prompt 或觸發不安全工作流。

## 來源與待追蹤

已確認來源：

- Claude Code skills：`https://code.claude.com/docs/en/skills`
- Claude Code plugins：`https://code.claude.com/docs/en/plugins-reference`
- OpenCode skills：`https://opencode.ai/docs/skills/`
- OpenCode rules：`https://opencode.ai/docs/rules/`
- OpenCode agents：`https://opencode.ai/docs/agents/`
- Kilo Code complete docs / llms：`https://kilo.ai/docs/llms.txt`
- Kilo Code custom rules：`https://kilo.ai/docs/customize/custom-rules`
- Kilo Code custom modes：`https://kilo.ai/docs/customize/custom-modes`
- Codex skills：`https://developers.openai.com/codex/skills.md`
- Codex AGENTS.md：`https://developers.openai.com/codex/guides/agents-md.md`
- Codex customization：`https://developers.openai.com/codex/concepts/customization.md`
- Cline rules：`https://docs.cline.bot/customization/cline-rules`
- Cursor rules：`https://cursor.com/docs/rules`

待後續下載前再確認：

- Kilo Code 對 `.claude/skills/` compatibility 在使用者實際安裝版本中是否預設啟用。
- OpenCode 對 skill frontmatter 欄位是否會拒絕缺少 `name` 或 `description` 的第三方 skill。
- Windows symlink / junction 是否可被各 agent 正確追蹤。
- Cline 最新 Skills 文件是否已支援 `SKILL.md` runtime 目錄；本輪只確認 rules 目錄。
- Cursor 是否有新增 Agent Skills 支援；目前不應假設 `.agents/skills/` 會被 Cursor 讀取。
