# FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW 使用說明（Kilo Code）

這份文件是給使用者看的操作指南：當你在 Kilo Code 裡要對已經 `git add` 的前端修改做「重型、多 sub-agent、可補位」review 時，如何啟用 `frontend-heavy-staged-review-workflow`。

## 1. 這個 workflow 是做什麼的？

`FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW` 是 `frontend-staged-review-workflow` 的重型版本。

它的目標不是修改 code，而是讓 Kilo 完成：

1. 只讀取已 staged 的內容：`git diff --cached`。
2. 建立 runtime config 與 dispatch plan。
3. 依 staged diff 選擇精確的 local review skills。
4. 每個選中的 review skill 預設派 5 個獨立 sub-agent。
5. 如果 reviewer 掛掉、逾時、輸出格式錯誤或沒有真正用到 skill，就用 replacement reviewer 補位。
6. 驗證每個 reviewer 的 strict JSON output。
7. 用 reviewer health ledger 與 skill quorum status 防止 overclaim。
8. 彙整 findings 後，再派 aggregation validator sub-agents 檢查最終報告。
9. 明確排除 unit test / test coverage 建議。

簡單說：

```text
先 git add 你要 review 的檔案。
再叫 Kilo 使用 frontend-heavy-staged-review-workflow。
Kilo 只 review staged diff，不改檔、不 commit。
每個 selected review skill 預設要有 5 個有效 reviewer。
```

## 2. 什麼時候應該使用？

適合以下情境：

- 你準備 commit 前，想做比一般 staged review 更嚴格的檢查。
- 修改風險高、範圍大、牽涉多個前端技術面。
- 你想讓多個 sub-agent 從不同角度獨立 review。
- 你希望 sub-agent 掛掉或輸出無效時，有 replacement reviewer 補位。
- 你希望 final report 有 quorum / degraded / incomplete 狀態，不會假裝完成。

不適合以下情境：

- 還沒有 `git add` 任何檔案。
- 想 review unstaged `git diff`。
- 只想快速 review；這時用 `frontend-staged-review-workflow` 即可。
- 想讓 agent 自動修復、stage 或 commit。
- 還在需求釐清或實作前規劃；這時應使用 `frontend-task-preflight`。

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

可以在 Kilo Code prompt 裡指定：

```text
請使用 frontend-heavy-staged-review-workflow skill。
```

更保險的寫法：

```text
請使用 frontend-heavy-staged-review-workflow skill，並遵守 Frontend Heavy Staged Review Rule。
只 review git diff --cached，不要 review unstaged changes，不要修改檔案，不要提出 unit test 建議。
每個 selected review skill 預設需要 5 個有效 reviewer；sub-agent 掛掉或輸出無效時請使用 replacement reviewer 補位。
```

## 4. 最推薦的 prompt 模板

```text
請使用 frontend-heavy-staged-review-workflow skill。

目標：
Review 我目前已經 git add 的前端修改，使用重型多 sub-agent review。

限制：
- 只 review `git diff --cached`。
- 不要 review unstaged changes；如果有，請列為 out of scope。
- 不要修改檔案。
- 不要 stage、commit 或 auto-fix。
- 不要提出 unit test 或 test coverage 建議。

Runtime config：
- reviewers_per_skill: 5
- replacement_budget_per_skill: 3
- aggregation_validator_count: 2
- primary_reviewer_isolation: true

請先輸出 runtime config 和 dispatch plan，然後分 wave 使用 sub-agent review。
每個 selected review skill 預設要有 5 個 valid reviewer outputs。
如果 reviewer failed / timed_out / invalid / missing，請用 replacement reviewer 補位。

最後請輸出：
1. Workflow status
2. Verdict
3. Runtime config
4. Dispatch Plan
5. Deferred / Dropped Skill Decisions
6. Reviewer Health Ledger
7. Skill Quorum Status
8. Aggregation Validation
9. Consolidated Findings
10. Aggregation Decision Log
11. Out of Scope
12. Suggested Fix Order

每個 finding 都要包含 path、severity、evidence、why it matters、recommended fix。
```

## 5. 自訂 reviewer 數量

可以要求更少或更多 reviewer：

```text
請使用 frontend-heavy-staged-review-workflow，reviewers_per_skill=7，replacement_budget_per_skill=4，allow_degraded_report=true。
```

或較省成本：

```text
請使用 frontend-heavy-staged-review-workflow，但 reviewers_per_skill=3，replacement_budget_per_skill=2。
```

## 6. 最短可用 prompt

```text
請使用 frontend-heavy-staged-review-workflow skill review 我已 staged 的前端修改。
只看 git diff --cached，不要改檔，不要提出 unit test 建議。
每個 selected review skill 預設跑 5 個有效 reviewer，失敗請補 replacement reviewer。
最後請列出 quorum 狀態、path、severity、evidence、recommended fix。
```

## 7. 使用前檢查

在呼叫 Kilo 前，建議你先確認：

```bash
git status --short
git diff --cached --name-only
```

如果 `git diff --cached --name-only` 沒有任何輸出，代表目前沒有 staged files，workflow 會停止。

## 8. 和其他 workflow 的差異

| Workflow | 使用時機 | sub-agent 強度 | 是否修改 code | 主要輸出 |
|---|---|---:|---|---|
| `frontend-task-preflight` | 開始實作前，需求/設計/方案還需要釐清 | 視情況 | 不修改 | implementation plan |
| `frontend-staged-review-workflow` | 一般 commit 前 staged diff review | 每個 selected skill 至少 2 個 reviewer | 不修改 | staged diff review report |
| `frontend-heavy-staged-review-workflow` | 高風險或需要更保險的 staged diff review | 每個 selected skill 預設 5 個 reviewer + replacement + aggregation validators | 不修改 | quorum-aware heavy review report |

## 9. Review 後怎麼接？

如果 verdict 是 `Request changes`：

1. 先修 critical/high findings。
2. 重新 `git add` 修正後的檔案。
3. 再跑一次 heavy workflow 或一般 staged review workflow。

如果 verdict 是 `Comment`：

1. 評估 medium/low findings 是否需要修。
2. 如果修了，重新 stage 並 rerun workflow。
3. 如果不修，在 commit message 或 PR note 裡記錄取捨。

如果 verdict 是 `Approve` 且 workflow status 是 `Complete` 或 `Complete with replacements`：

1. 可以進入 commit / PR 流程。
2. 若工作區還有 unstaged changes，記得那些沒有被本 workflow review。

如果 workflow status 是 `Incomplete` 或 `Degraded`：

1. 先看 Skill Quorum Status 和 Reviewer Health Ledger。
2. 確認是哪個 skill 沒達到 reviewer quorum。
3. 可提高 replacement budget 後重跑，或明確接受 degraded report。
