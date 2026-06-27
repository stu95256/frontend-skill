# FRONTEND_STAGED_REVIEW_WORKFLOW 使用說明（Kilo Code）

這份文件是給使用者看的操作指南：當你在 Kilo Code 裡要 review 已經 `git add` 的前端修改時，如何啟用 `frontend-staged-review-workflow`。

## 1. 這個 workflow 是做什麼的？

`FRONTEND_STAGED_REVIEW_WORKFLOW` 是「前端 staged diff review」工作流。

它的目標不是修改 code，而是先讓 agent 完成：

1. 只讀取已 staged 的內容：`git diff --cached`。
2. 建立 internal review dispatch plan。
3. 依 staged diff 選擇精確的 local review skills。
4. 每個選中的 review skill 至少派 2 個獨立 sub-agent。
5. 驗證每個 reviewer 的輸出。
6. 彙整成一份包含 path、severity、evidence、recommended fix 的報告。
7. 明確排除 unit test 建議。

簡單說：

```text
先 git add 你要 review 的檔案。
再叫 Kilo 使用 frontend-staged-review-workflow。
Kilo 只 review staged diff，不改檔、不 commit。
```

## 2. 什麼時候應該使用？

適合以下情境：

- 你已經完成一段前端修改，想在 commit 前 review。
- 你只想 review `git add` 後的內容，不想把工作區其他變更混進來。
- 你希望多個 sub-agent 從不同角度檢查同一份 staged diff。
- 修改涉及 React、TypeScript、Tailwind、Ant Design、AG Grid、react-hook-form、react-i18next、React Router、accessibility、responsive、UI/UX 或 browser behavior。
- 你希望最後報告有清楚的 path、severity、recommended fix。

不適合以下情境：

- 還沒有 `git add` 任何檔案。
- 想 review unstaged `git diff`。
- 想讓 agent 自動修復、stage 或 commit。
- 只想討論需求或做實作前規劃；這時應使用 `frontend-task-preflight`。

## 3. 在 Kilo Code 裡怎麼啟用？

如果你已經把 `.kilo` 資料夾移到：

```text
~/.kilo
```

並且在 Kilo global config 裡設定：

```jsonc
{
  "skills": {
    "paths": [
      "~/.kilo/skills"
    ]
  },
  "instructions": [
    "~/.kilo/rules/*.md"
  ]
}
```

那你可以在 Kilo Code prompt 裡直接指定：

```text
請使用 frontend-staged-review-workflow skill。
```

更保險的寫法是：

```text
請使用 frontend-staged-review-workflow skill，並遵守 Frontend Staged Review Rule。
只 review git diff --cached，不要 review unstaged changes，不要修改檔案，不要提出 unit test 建議。
```

## 4. 最推薦的 prompt 模板

```text
請使用 frontend-staged-review-workflow skill。

目標：
Review 我目前已經 git add 的前端修改。

限制：
- 只 review `git diff --cached`。
- 不要 review unstaged changes；如果有，請列為 out of scope。
- 不要修改檔案。
- 不要 stage、commit 或 auto-fix。
- 不要提出 unit test 或 test coverage 建議。

請建立 internal dispatch plan，不需要輸出；然後必須實際啟動 Kilo sub-agent/custom agent 或等價 sub-agent 工具進行 review。
每個選中的 review skill 至少要有 2 個獨立 reviewer。
不要由主 agent/coordinator 自己扮演多個 reviewer；如果目前環境無法啟動真實 sub-agent，請回報 Incomplete，不要改用主 agent 單獨 review。

最後請只輸出 findings 相關內容：
1. Verdict
2. Findings grouped by severity: Critical / High / Medium / Low
3. Suggested Fix Order

每個 finding 都要包含 path、severity、evidence、why it matters、recommended fix。
不要輸出 Dispatch Plan、Reviewer Ledger、Aggregation Decision Log、reviewer ID、sub-agent 來源或 skill 來源。
```

## 5. 最短可用 prompt

```text
請使用 frontend-staged-review-workflow skill review 我已 staged 的前端修改。
只看 git diff --cached，不要改檔，不要提出 unit test 建議。
必須實際使用 Kilo sub-agent/custom agent 或等價 sub-agent 工具；不要由主 agent 自己模擬多個 reviewer。若無法啟動真實 sub-agent，請回報 Incomplete。
最後回覆請使用中文，且只輸出 findings：path、severity、evidence、why it matters、recommended fix；不要輸出 reviewer/sub-agent/skill 來源。
```

## 6. 使用前檢查

在呼叫 Kilo 前，建議你先確認：

```bash
git status --short
git diff --cached --name-only
```

如果 `git diff --cached --name-only` 沒有任何輸出，代表目前沒有 staged files，workflow 會停止。

## 7. 和 frontend-task-preflight 的差異

| Workflow | 使用時機 | 是否修改 code | 主要輸出 |
|---|---|---|---|
| `frontend-task-preflight` | 開始實作前，需求/設計/方案還需要釐清 | 不修改 | implementation plan |
| `frontend-staged-review-workflow` | 實作後、commit 前，已經 `git add` 要 review 的修改 | 不修改 | staged diff review report |

## 8. Review 後怎麼接？

如果 verdict 是 `Request changes`：

1. 先修 critical/high findings。
2. 重新 `git add` 修正後的檔案。
3. 再跑一次 `frontend-staged-review-workflow`。

如果 verdict 是 `Comment`：

1. 評估 medium/low findings 是否需要修。
2. 如果修了，重新 stage 並 rerun workflow。
3. 如果不修，在 commit message 或 PR note 裡記錄取捨。

如果 verdict 是 `Approve`：

1. 你可以進入 commit / PR 流程。
2. 若工作區還有 unstaged changes，記得那些沒有被本 workflow review。
