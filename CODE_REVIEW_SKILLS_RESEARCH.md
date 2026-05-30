# Code Review Skills 調查與安裝紀錄

搜尋日期：2026-05-29

## 目的

本次調查目標是為之後大量使用 sub-agent review 做準備：先盤點本專案目前已經有的 review / quality 類 skills，再搜尋網路上推薦、較多人使用、或內容明顯更適合 sub-agent review 的 `SKILL.md`，最後將授權與內容合適的項目安裝到本專案 `skills/` staging 目錄。

## 本專案目前已有的 review / quality 類重點 skills

本專案已經有不少 review 與品質 gate：

| Skill | 來源 | 用途 |
|---|---|---|
| `code-review-excellence` | `awesome-skills/code-review-skill` | 大型通用 review skill；含 React、TypeScript、CSS、architecture、security、performance 多語言/多框架參考。 |
| `typescript-code-reviewer` | project-curated | TypeScript / TSX 專用 reviewer；檢查 `any`/`unknown`、unsafe assertions、strict tsconfig、async/error handling、React hooks、XSS 與測試覆蓋。 |
| `code-review-and-quality` | `addyosmani/agent-skills` | 五軸 review：correctness、readability、architecture、security、performance；適合 merge 前品質 gate。 |
| `requesting-code-review` | `obra/superpowers` | 開發完成後派 reviewer sub-agent；強調 reviewer 使用獨立 context。 |
| `receiving-code-review` | `obra/superpowers` | 收到 review 後先分析與驗證，不盲目接受。 |
| `verification-before-completion` | `obra/superpowers` | 宣稱完成前必須跑驗證。 |
| `security-and-hardening` | `addyosmani/agent-skills` | 安全 hardening；作為 security reviewer 的補充。 |
| `web-design-guidelines` | `vercel-labs/agent-skills` | UI / UX / accessibility review。 |
| `playwright-best-practices` | `currents-dev/playwright-best-practices-skill` | E2E、component、visual、a11y、security、CI 等 Playwright review/測試準則。 |

結論：目前一般 code review、TypeScript review、UI/test review 已經足夠；本次新增主要補兩個缺口：

1. 讓 sub-agent 可以做「平行多 reviewer audit」的協調 skill。
2. 補上研究型、false-positive 抑制較強的 security + privacy review methodology。

## 搜尋方法

使用 GitHub Search API 與 raw `SKILL.md` 檢查，查詢字串包含：

```text
"code review" "SKILL.md"
"security" "code review" "SKILL.md"
"review" "Claude Code" "SKILL.md"
"code-review" "SKILL.md" "Claude"
```

優先判斷條件：

- 是否有明確 LICENSE 或檔案內授權。
- 是否是標準 `SKILL.md`，不是單純 prompt、slash command 或 MCP。
- 是否補足本專案缺口，而非與既有 `code-review-excellence` / `typescript-code-reviewer` 重複。
- 是否適合 sub-agent review：可拆 pass、可輸出結構化 findings、可作為 merge/release gate。

## 候選來源與判斷

| Repository / Skill | Stars（搜尋時） | License | 判斷 |
|---|---:|---|---|
| `facebookresearch/secpriv-skill` / root `SKILL.md` | 3 | MIT | 已安裝為 `secpriv-code-review`。雖然 stars 少，但來源是 Meta / Facebook Research，README 記錄 128-case benchmark；重點是 security + privacy 合一、CWE/GDPR mapping、detector-validator、confidence threshold，適合安全/隱私 reviewer sub-agent。 |
| `vosslab/vosslab-skills` / `skills/audit-code-reviewer` | 2 | MIT | 已安裝為 `audit-code-reviewer`。它明確要求 6 個獨立 sub-agent pass，再由主 agent 彙整 findings，正好符合本專案後續大量使用 sub-agent review 的需求。 |
| `mamamou/ai-coding-skills` / `code-reviewer-react`、`code-reviewer`、`security-auditor` | 14 | GitHub API 未標示 repo license；個別 skill frontmatter 寫 MIT | 暫不直接安裝。內容看起來很完整，尤其 React overlay 覆蓋 React 17/18/19、RSC、React Compiler、TanStack Query、Zustand、React Hook Form；但 repo 層級 license 不明，且與既有 `typescript-code-reviewer`、`code-review-excellence` 部分重疊。後續若要補 React 專用 reviewer，可參考官方文件另建 project-curated skill。 |
| `irfad7/claude-power-skills` / `code-review`、`security-review` | 4 | MIT | 暫不安裝。內容是清楚的 multi-pass senior review，但與 `code-review-excellence`、`code-review-and-quality`、`security-and-hardening` 高度重疊。 |
| `setmpp/claude-code-skills` / `skills/code-review` | 0 | MIT | 暫不安裝。簡潔、好用，但與既有通用 review skill 重疊。 |
| `kakarot-oncloud/claude-dev-skills` / `skills/code-reviewer` | 0 | MIT | 暫不安裝。適合 senior review output format，但內容較短，與既有技能重複。 |
| `shaunlatip/converge` / root `SKILL.md` | 0 | MIT | 暫不安裝。它是 iterative review + fix loop orchestrator，不是純 reviewer；有價值但會驅動修改檔案，之後若要做自動修復閉環可再加入。 |
| `BigPapiCB/Universal-Claude-Skills` / `code-review`、`security-audit` | 2 | repo license 未明 | 暫不安裝。無明確 repo license，且內容與既有 skill 重疊。 |
| `thelycorisdesignstudio/claude-skills` | 2 | repo license 未明 | 暫不安裝。無明確 repo license。 |
| `jooooonj/develop-agent` / `code-review` | 0 | repo license 未明 | 暫不安裝。無明確 repo license。 |
| `Vaughanwj/Agent-Skills` / `healthcare-secure-code-review` | 0 | NOASSERTION | 暫不安裝。偏 healthcare domain 且授權不清。 |
| `gitstq/awesome-ai-agent-skills` / `super-reviewer` | 1 | MIT | 暫不安裝。看起來偏「4 個 production-grade skills」集合，但本次優先選擇更明確的 vosslab parallel reviewer 與 Meta SecPriv。 |

## 本次安裝

### `skills/audit-code-reviewer/`

來源：

- Repo: https://github.com/vosslab/vosslab-skills
- Commit: `8382b5e830530db393b8a1fe2891a12cd41dd1e8`
- Source path: `skills/audit-code-reviewer`
- License: MIT

用途：

- 在 merge 或 release 前，讓主 agent 只做最小 preflight，然後派出多個獨立 reviewer sub-agents。
- 適合後續 reviewer 分工：correctness、tests、security、architecture、frontend/runtime、docs/operability 等 pass。
- 回收 sub-agent 結果後，主 agent 彙整 severity、去重、標示 residual risk。

### `skills/secpriv-code-review/`

來源：

- Repo: https://github.com/facebookresearch/secpriv-skill
- Commit: `5e5c2cac9c95143faee7560d6719209c8c2d8900`
- Source path: `SKILL.md`
- License: MIT

用途：

- 針對安全弱點與隱私違規做單一 review pass。
- 將 findings 對應到 CWE 與 GDPR basis。
- 使用 detector-validator methodology 與 confidence threshold，降低 false positives。
- 適合交給專門 security/privacy reviewer sub-agent，輸出 JSON findings 給 coordinator 彙整。

注意：upstream root `SKILL.md` 沒有 YAML frontmatter；本專案 staging copy 在檔案開頭加入 `name` / `description` / `version` / `license` / `metadata` frontmatter，以符合本專案 `skills/<skill-name>/SKILL.md` 驗證規則，其餘 methodology 內容保留。

## 建議的 sub-agent review 組合

之後做大型前端任務 review，可以依任務大小選：

### 快速 review

- `code-review-and-quality`
- `typescript-code-reviewer`

### 前端 PR / AI 產生 code 的一般 review

- `code-review-excellence`
- `typescript-code-reviewer`
- `web-design-guidelines`（如果有 UI/UX 變更）
- `playwright-best-practices` 或 `webapp-testing`（如果有 browser behavior / E2E 風險）

### merge / release 前的平行 sub-agent audit

- `audit-code-reviewer` 作為 coordinator skill。
- 子 reviewer 可分配：
  - `typescript-code-reviewer`：TypeScript / TSX / React hooks / strictness。
  - `secpriv-code-review`：security + privacy。
  - `code-review-excellence`：general correctness、architecture、performance。
  - `web-design-guidelines`：UI / accessibility。
  - `playwright-best-practices`：E2E / browser runtime / flakiness。
  - `verification-before-completion`：最後驗證與 evidence gate。

## 後續可再研究

- 如果確認 `mamamou/ai-coding-skills` 的 repo 層級 LICENSE 或作者授權，可考慮加入 `code-reviewer-react`；它對 React 17/18/19 與 ecosystem 的版本感知規則很完整。
- 如果要做自動修復閉環，可研究 `shaunlatip/converge`，但它會把 review + fix loop 組合成 orchestrator，需先決定是否允許 review skill 主動修改檔案。

## 2026-05-29 補充：frontend staged review workflow

已新增本專案自有 workflow skill：`skills/frontend-staged-review-workflow/`。

此 workflow 專門 review 已 staged 的前端修改：

- 目標固定為 `git diff --cached`，不 review unstaged files。
- 每個被選中的 review skill 至少派 2 個獨立 sub-agent。
- 每個 sub-agent 都要宣告使用的 exact local skill，並回傳 structured findings。
- 主 agent 建立 reviewer ledger，整理每個 sub-agent 的回傳結果，再去重、正規化 severity。
- 最終報告必須列出 path、severity、issue、why it matters、recommended fix。
- 依使用者要求，workflow 明確禁止 unit test 建議，彙整時也會移除 unit-test-only finding。

研究來源包含 Anthropic Claude Code subagents docs、GitHub PR review docs、Google Engineering Practices、SmartBear review practices，以及本專案已安裝的 `audit-code-reviewer` / `secpriv-code-review`。詳細記錄在 `skills/frontend-staged-review-workflow/references/research-notes.md`。
