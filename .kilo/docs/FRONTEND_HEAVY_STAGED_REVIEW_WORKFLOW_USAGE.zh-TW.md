# FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW 使用說明（Kilo Code）

這份文件是給使用者看的操作指南：當你在 Kilo Code 裡要對已經 `git add` 的前端修改做「重型、多 sub-agent、可補位」review 時，如何啟用 `frontend-heavy-staged-review-workflow`。

## 1. 這個 workflow 是做什麼的？

`FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW` 是 `frontend-staged-review-workflow` 的重型版本。

它的目標不是修改 code，而是讓 Kilo 完成：

1. 只讀取已 staged 的內容：`git diff --cached`。
2. 建立 internal runtime config 與 internal dispatch plan。
3. 依 staged diff 選擇精確的 local review skills。
4. 每個選中的 review skill 預設派 5 個真實、獨立 sub-agent。
5. 如果 reviewer 掛掉、逾時、輸出格式錯誤或沒有真正用到 skill，就用 replacement reviewer 補位。
6. 驗證每個 reviewer 的 strict JSON output。
7. 用 internal reviewer health ledger 與 skill quorum status 防止 overclaim。
8. 彙整 findings 後，再派 aggregation validator sub-agents 檢查 findings。
9. 明確排除 unit test / test coverage 建議。
10. 最後只輸出 findings，不輸出 dispatch plan、ledger、reviewer 來源或 skill 來源。

簡單說：

```text
先 git add 你要 review 的檔案。
再叫 Kilo 使用 frontend-heavy-staged-review-workflow。
Kilo 只 review staged diff，不改檔、不 commit。
每個 selected review skill 預設要有 5 個有效 reviewer。
最後只回 findings。
```

## 2. 什麼時候應該使用？

適合以下情境：

- 你準備 commit 前，想做比一般 staged review 更嚴格的檢查。
- 修改風險高、範圍大、牽涉多個前端技術面。
- 你想讓多個 sub-agent 從不同角度獨立 review。
- 你希望 sub-agent 掛掉或輸出無效時，有 replacement reviewer 補位。
- 你希望 workflow 不會在 quorum 失敗時假裝完成。

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
必須實際啟動 Kilo sub-agent/custom agent 或等價 sub-agent 工具；不要由主 agent 自己模擬多個 reviewer。
每個 selected review skill 預設需要 5 個有效 reviewer；sub-agent 掛掉或輸出無效時請使用 replacement reviewer 補位。
最後回覆請使用中文；只輸出 findings，不要輸出 reviewer/sub-agent/skill 來源。
```

## 4. 最推薦的 prompt 模板

```text
請使用 frontend-heavy-staged-review-workflow skill。

目標：
Review 我目前已經 git add 的前端修改，使用重型多 sub-agent review。

限制：
- 只 review `git diff --cached`。
- 不要 review unstaged changes；如果有，請列為 internal out of scope，不要拿來 review。
- 不要修改檔案。
- 不要 stage、commit 或 auto-fix。
- 不要提出 unit test 或 test coverage 建議。

Runtime config：
- reviewers_per_skill: 5
- replacement_budget_per_skill: 3
- aggregation_validator_count: 2
- primary_reviewer_isolation: true
- final_report: findings_only

請建立 internal runtime config 和 internal dispatch plan，不需要輸出。
必須實際啟動 Kilo sub-agent/custom agent 或等價 sub-agent 工具進行 review。
每個 selected review skill 預設要有 5 個 valid reviewer outputs。
如果 reviewer failed / timed_out / invalid / missing，請用 replacement reviewer 補位。
不要由主 agent/coordinator 自己扮演多個 reviewer；如果目前環境無法啟動真實 sub-agent，請回報 Incomplete，不要改用主 agent 單獨 review。

最後回覆請使用中文，且只輸出 findings 相關內容：
1. Verdict
2. Findings grouped by severity: Critical / High / Medium / Low
3. Suggested Fix Order

每個 finding 都要包含 path、severity、evidence、why it matters、recommended fix。
不要輸出 Runtime config、Dispatch Plan、Reviewer Health Ledger、Skill Quorum Status、Aggregation Decision Log、reviewer ID、sub-agent 來源或 skill 來源。
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
必須實際使用 Kilo sub-agent/custom agent 或等價 sub-agent 工具；不要由主 agent 自己模擬多個 reviewer。若無法啟動真實 sub-agent，請回報 Incomplete。
每個 selected review skill 預設跑 5 個有效 reviewer，失敗請補 replacement reviewer。
最後回覆請使用中文，且只輸出 findings：path、severity、evidence、why it matters、recommended fix；不要輸出 reviewer/sub-agent/skill 來源。
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
| `frontend-staged-review-workflow` | 一般 commit 前 staged diff review | 每個 selected skill 至少 2 個 reviewer | 不修改 | findings-only staged review report |
| `frontend-heavy-staged-review-workflow` | 高風險或需要更保險的 staged diff review | 每個 selected skill 預設 5 個 reviewer + replacement + aggregation validators | 不修改 | findings-only quorum-aware heavy review report |

## 9. Review 後怎麼接？

如果 verdict 是 `Request changes`：

1. 先修 critical/high findings。
2. 重新 `git add` 修正後的檔案。
3. 再跑一次 heavy workflow 或一般 staged review workflow。

如果 verdict 是 `Comment`：

1. 評估 medium/low findings 是否需要修。
2. 如果修了，重新 stage 並 rerun workflow。
3. 如果不修，在 commit message 或 PR note 裡記錄取捨。

如果 verdict 是 `Approve`：

1. 可以進入 commit / PR 流程。
2. 若工作區還有 unstaged changes，記得那些沒有被本 workflow review。

如果 verdict 是 `Incomplete` 或 `Degraded`：

1. 可重跑 workflow。
2. 或要求 Kilo 輸出 audit log，確認哪個 skill / reviewer quorum 沒達標。
3. 可提高 replacement budget 後重跑，或明確接受 degraded report。
