# FRONTEND_BRANCH_REVIEW_WORKFLOW 使用說明（Kilo Code）

這份文件說明如何 review 某個 frontend branch 將要合併進 `master` 的內容。

## 1. Workflow 的用途

`frontend-branch-review-workflow` 會：

1. 取得來源 branch 與目標 branch；目標預設為 `master`。
2. 將 source、target、merge base 固定成不可變的 commit SHA。
3. 只 review merge base 到 source tip 的 committed branch contribution。
4. 排除 working tree、staged、untracked 與單純 target-only 的修改。
5. 依變更內容選擇精確的 local review skills。
6. 每個 selected review skill 至少啟動 2 個真實獨立 sub-agent。
7. 驗證 reviewer output 與三個 pinned SHAs。
8. 回傳精簡的中文 findings-only 報告。

核心範圍是：

```bash
git diff --find-renames <merge-base-sha> <source-sha>
```

不是：

```bash
git diff --cached
git diff master..feature-branch
```

## 2. 和 staged review 的差異

| Workflow | Review 對象 | 是否包含未 commit 內容 | 適用時機 |
|---|---|---:|---|
| `frontend-staged-review-workflow` | `git diff --cached` | staged 內容會包含 | commit 前 review 已 `git add` 的修改 |
| `frontend-branch-review-workflow` | merge base → source branch tip | 不包含 | branch 準備 merge 進 `master` 前 |
| `frontend-heavy-staged-review-workflow` | `git diff --cached` | staged 內容會包含 | 需要每個 skill 5 個 reviewer 的重型 staged review |

## 3. 使用前準備

確認來源 branch 已包含所有要 review 的 committed changes：

```bash
git status --short --branch
git log --oneline master..your-source-branch
```

未 commit、staged 或 untracked 內容不會進入 branch review。

如果使用 remote branch，可以指定：

```text
origin/feature/order-filter
```

Workflow 不需要 checkout 該 branch，也不會執行 merge、rebase 或 reset。

## 4. 推薦 Prompt

```text
請使用 frontend-branch-review-workflow skill。

來源 branch：feature/order-filter
目標 branch：master

請 review 來源 branch 將要合併進 master 的 committed frontend changes。

範圍與安全規則：
- 先將 source、target、merge base resolve 成 pinned commit SHAs。
- 只 review merge base 到 source SHA 的 branch contribution。
- 如果可以，先 fetch 最新 origin/master 並以 origin/master 作為 effective target；如果不能 fetch，請記錄 target freshness。
- 不要把 working tree、staged、untracked 或 target-only changes 當成 branch findings。
- 需要完整檔案內容時，請用 git show <sha>:<path>，不要假設目前 checkout 的檔案就是來源 branch。
- 不要 checkout、switch、merge、rebase、reset、修改檔案、stage、auto-fix 或 commit。
- 不要提出 unit test 或 test coverage 建議。

Sub-agent 規則：
- 先建立 internal dispatch plan，不需要輸出。
- 必須實際啟動 Kilo sub-agent/custom agent 或等價 sub-agent 工具。
- 每個 selected review skill 至少需要 2 個有效獨立 reviewer。
- 主 agent/coordinator 不可以扮演多個 reviewer。
- Reviewer output 必須對應相同的 source SHA、target SHA 與 merge-base SHA。
- 如果無法啟動真實 sub-agent 或 reviewer quorum 不足，請回報 Incomplete。

最後只輸出中文 findings：
- 審查範圍（source/target refs 與 short SHAs）
- Verdict
- Findings grouped by severity
- 每個 finding 的 path、line、issue、evidence、impact、recommended fix
- Suggested Fix Order（有多個 findings 時）

不要輸出 Dispatch Plan、Reviewer Ledger、reviewer ID、sub-agent/skill 來源、retry 或 aggregation log。
```

## 5. 最短 Prompt

```text
請使用 frontend-branch-review-workflow review `feature/order-filter` 將要合併進 `master` 的內容。
只 review merge base 到 source tip 的 committed changes，不要包含 working tree/staged/untracked/target-only changes，也不要改檔或提出 unit test 建議。
每個 selected review skill 至少使用 2 個真實獨立 sub-agent；主 agent 不可模擬 reviewer，無法達成時回報 Incomplete。
最後用中文只輸出 branch scope、verdict 與 findings。
```

## 6. 使用 current branch

如果目前 checkout 的 branch 就是來源，可以省略來源 branch：

```text
請使用 frontend-branch-review-workflow review 目前 branch 將要合併進 master 的內容。
```

如果目前是 detached HEAD，workflow 不會猜來源 branch，會要求你明確提供 source ref。

## 7. Review Snapshot

Workflow 會固定三個 SHA：

- `source_sha`：來源 branch tip；
- `target_sha`：有效目標 branch tip；
- `merge_base_sha`：兩者共同祖先。

Review 執行期間即使 branch ref 移動，也不會偷偷切換範圍。要 review 新的 branch tip，必須重新執行 workflow。

最終報告會顯示類似：

```text
審查範圍: feature/order-filter@a1b2c3d → origin/master@d4e5f6a
```

## 8. Verdict

- `Request changes`：有 critical/high blocking finding。
- `Comment`：只有 medium/low findings。
- `Approve`：沒有 findings，且 coverage、sub-agent quorum、snapshot validation 全部完成。
- `Incomplete`：ref/merge-base/snapshot/coverage/sub-agent/quorum 任一必要條件未完成。

## 9. Review 後續

如果是 `Request changes`：

1. 在 source branch 修正 findings。
2. Commit 修正。
3. 重新跑 workflow，讓它 pin 新的 source SHA。

如果是 `Approve`：

1. 可以進入 PR 或 merge 流程。
2. 注意在 review 後新增的 commit 沒有被這次 snapshot review。
3. 真正 merge 前若 `master` 又有變更，建議重新執行一次。
