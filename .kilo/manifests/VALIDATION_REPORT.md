# Skills Validation Report

日期：2026-05-30

## 結果摘要

- 安裝位置：`skills/`
- skill 目錄數：65
- 檔案數：425
- `SKILL.md` frontmatter 檢查：通過
- `name` 與目錄名稱一致性：通過
- 高風險 shell 命令掃描：未發現真實高風險命令；掃描規則本身不列入命中
- secret / token 掃描：沒有發現真實 token；命中皆為文件與測試範例 false positives

## 本次新增

- `typescript-code-reviewer`：本專案整理的 TypeScript / TSX 專用 code reviewer skill。
  - 位置：`skills/typescript-code-reviewer/SKILL.md`
  - 研究紀錄：`skills/typescript-code-reviewer/references/research-sources.md`
  - 簡版 checklist：`skills/typescript-code-reviewer/references/checklist.md`
  - 授權策略：未直接複製沒有明確授權的遠端 TypeScript code review skill；內容依官方文件與 MIT/Apache-2.0 來源整理。

- `playwright-mcp-usage`：使用者提供的 Playwright MCP 使用流程；在一般網路搜尋被阻擋時，透過真實瀏覽器做 DOM 讀取、截圖檢查與受控互動。
  - 位置：`skills/playwright-mcp-usage/SKILL.md`
  - 來源：user-provided attached file `Z:/新.txt`

- `audit-code-reviewer`：MIT 授權的平行多 reviewer audit skill，適合 merge/release 前由 coordinator 派多個 sub-agent 獨立 review。
  - 位置：`skills/audit-code-reviewer/SKILL.md`
  - 來源：`vosslab/vosslab-skills` commit `8382b5e830530db393b8a1fe2891a12cd41dd1e8`

- `secpriv-code-review`：Meta / Facebook Research 的 SecPriv security + privacy review skill；本專案加上相容 frontmatter 後 staging。
  - 位置：`skills/secpriv-code-review/SKILL.md`
  - 來源：`facebookresearch/secpriv-skill` commit `5e5c2cac9c95143faee7560d6719209c8c2d8900`
  - 授權策略：upstream MIT；root `SKILL.md` 原本無 YAML frontmatter，因此本專案僅新增 frontmatter 與 staging note，保留原 methodology。

- `frontend-staged-review-workflow`：本專案整理的前端 staged diff review workflow；只 review `git diff --cached`，每個選用 review skill 至少 2 個 sub-agent，並排除 unit test 建議。
  - 位置：`skills/frontend-staged-review-workflow/SKILL.md`
  - 研究紀錄：`skills/frontend-staged-review-workflow/references/research-notes.md`
  - 模板：`skills/frontend-staged-review-workflow/templates/subagent-prompt.md`、`skills/frontend-staged-review-workflow/templates/final-report.md`
  - 授權策略：project-curated MIT；引用外部 workflow 文件與本專案既有 local review skills，不直接 vendoring 第三方內容。

- `frontend-debug-workflow`：本專案整理的前端 debug workflow；使用者提供程式碼位置與問題後，先讀指定檔案與附近使用、收集 evidence、形成 root cause hypothesis，再選 exact local frontend skills 做最小修正與驗證。
  - 位置：`skills/frontend-debug-workflow/SKILL.md`
  - 完整 workflow：`FRONTEND_DEBUG_WORKFLOW.md`、`skills/frontend-debug-workflow/references/FRONTEND_DEBUG_WORKFLOW.md`
  - 研究紀錄：`skills/frontend-debug-workflow/references/research-notes.md`
  - 授權策略：project-curated MIT；引用外部 workflow / debugging 文件與本專案既有 local frontend skills，不直接 vendoring 第三方內容。

## Secret 掃描 false positives

以下命中皆為教學或測試範例，不是真實憑證：

| 檔案 / 類別 | 判定 |
|---|---|
| `code-review-excellence/reference/security-review-guide.md` | hardcoded password 反例示範 |
| `code-review-excellence/reference/java.md` | masked API key 教學片段 |
| `e2e-testing-patterns/references/details.md` | E2E test user sample password |
| `javascript-testing-patterns/references/advanced-testing-patterns.md` | test fixture / mock user password examples |
| `playwright-best-practices/advanced/authentication*.md` | Playwright auth test credentials / mock tokens |
| `playwright-best-practices/advanced/multi-context.md` | mock access token example |
| `playwright-best-practices/advanced/third-party.md` | Stripe mock payment secret example |
| `playwright-best-practices/infrastructure-ci-cd/ci-cd.md` | CI secret reference examples, not real values |
| `react-hook-form-zod/templates/server-validation.ts` | sample validation error payload |
| `security-and-hardening/SKILL.md` | intentionally demonstrates secret-scanning patterns |
| `typescript-code-reviewer/*` | references discuss secret handling and token scanning, no real credentials |
| `secpriv-code-review/SKILL.md` | security taxonomy documents `eval()` / `exec()` as vulnerabilities to detect; not an instruction to execute |

## 注意事項

這些 skills 是從第三方 upstream 或本專案整理後放到 staging 目錄。移植到 `.claude/skills/`、`.opencode/skills/` 或其他 agent runtime 前，仍建議依當前專案需求挑選子集，不要無差別全部安裝。
