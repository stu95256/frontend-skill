# VS Code Chat Custom Agents 中文使用指南

本文件說明何時選擇 user-facing Custom Agent、應附加哪些 Markdown，以及建議的輸入格式。安裝位置與 VM 移植方式請參考 [`VS_CODE_CHAT_SETUP.zh-TW.md`](./VS_CODE_CHAT_SETUP.zh-TW.md) 與 [`VM_COPY_GUIDE.zh-TW.md`](./VM_COPY_GUIDE.zh-TW.md)。

## 使用原則

本 catalog 只有以下五個 user-facing Agents：

| Agent | 適用情境 | 最重要的輸入 |
|---|---|---|
| Frontend Task Preflight | 實作前研究、釐清、方案與計畫 | 任務需求 MD、設計資料、限制 |
| Frontend Implementation | 執行已核准的計畫 | 已核准計畫、驗收條件、允許修改範圍 |
| Frontend Debug | 重現、定位並修正 frontend defect | 症狀、重現步驟、錯誤證據、相關路徑 |
| Frontend Review | staged、heavy staged 或 branch review | 明確 review mode 與 Git scope |
| VS Code Skill Creator | 建立或改善 Agent Skill | Skill 目標、正負觸發例、目的位置 |

`Frontend Researcher`、`Frontend Reviewer` 等 worker 設定為 `user-invocable: false`。不要在 Agent picker 直接尋找或選擇它們；coordinator 會透過 `agent/runSubagent` 呼叫。

## 如何提供 Markdown

推薦把本次任務資料寫成獨立 Markdown，例如：

```text
docs/tasks/TASK-123.md
```

然後在 VS Code Chat：

1. 選擇適合的 Custom Agent。
2. 使用 Chat 的附件／Add Context 功能加入該 Markdown，或在訊息中提供清楚的 workspace-relative path。
3. 貼上本文件對應的輸入模板。

只需要附加本次任務、計畫或錯誤證據。不要重複附加 `skills/**/SKILL.md` 或 workflow reference；Agent 會從已安裝的 catalog 載入它們。

不要在 Markdown 中放 API key、token、cookie、password、private key 或 connection string。

## 共用輸入欄位

複雜任務建議包含：

```markdown
# Goal
<!-- 要完成什麼，以及使用者可觀察到的結果 -->

# Context
<!-- 相關頁面、component、route、API、設計或 issue -->

# Relevant paths
<!-- workspace-relative paths；未知可寫「請先調查」 -->

# Current behavior
<!-- 現在發生什麼 -->

# Expected behavior
<!-- 應該發生什麼 -->

# Constraints
<!-- 不可改的 API、相容性、套件、設計、時程或安全限制 -->

# Acceptance criteria
- [ ] 可驗證條件 1
- [ ] 可驗證條件 2

# Verification
<!-- 期望執行的 test、lint、typecheck、build、browser checks -->

# Output
<!-- 希望得到計畫、實作、finding report 或 Skill package -->
```

缺少的 Repository 事實可以要求 Agent 先調查；不要為了填滿模板而猜測。

---

## Frontend Task Preflight

### 何時使用

需求尚未轉成可執行計畫，或需要先比較既有程式、Figma／設計、API 與產品行為時使用。這個 Agent 只產出核准前計畫，不直接實作。

### 建議附件

- 任務需求，例如 `TASK-123.md`
- Figma URL、截圖或設計說明
- API contract／OpenAPI path
- issue 或 acceptance criteria

### 最小輸入

```text
請根據附件 TASK-123.md 執行 frontend preflight。
先調查目前實作與相關路徑，列出阻塞問題、可行方案與取捨，最後產生可核准的 implementation plan。
本階段不要修改程式。
```

### 完整輸入模板

```markdown
請執行 Frontend Task Preflight。

## Requirement source
- 附件：`docs/tasks/TASK-123.md`
- Design：<URL 或「無」>
- Issue：<URL／編號或「無」>

## Starting scope
- 相關路徑：`src/...`
- 允許先調查相鄰程式：是
- 明確排除：`...`

## Decisions already made
- <不可重新決定的產品／技術決策>

## Questions to resolve
- <希望 preflight 回答的問題>

## Required plan quality
- 列出精確檔案與修改順序
- 包含 naming、accessibility、error handling 與 verification
- 若設計與現況不同，產生 gap matrix
- 只有真正阻塞的問題才詢問我

## Stop condition
只提交計畫供我核准；不要開始實作。
```

核准後使用 **Implement Approved Plan** handoff，或把輸出的計畫保存成 Markdown 再交給 `Frontend Implementation`。

---

## Frontend Implementation

### 何時使用

已經有明確且核准的 implementation plan，需要依序實作、驗證與 review 時使用。不要只提供模糊需求；模糊需求先進入 `Frontend Task Preflight`。

### 建議附件

- 已核准計畫，例如 `docs/plans/TASK-123-plan.md`
- 原始需求或 acceptance criteria
- 前次 review findings（若是修正回合）

### 最小輸入

```text
請實作附件 TASK-123-plan.md 中已核准的計畫。
只修改計畫允許的範圍，執行其中的驗證，完成後回報實際修改、命令結果與剩餘風險。
不要 commit 或 push。
```

### 完整輸入模板

```markdown
請執行 Frontend Implementation。

## Approved plan
- 附件：`docs/plans/TASK-123-plan.md`
- 計畫狀態：已核准

## Allowed changes
- `src/...`
- `tests/...`

## Forbidden changes
- 不修改：`...`
- 不新增 dependency／不改 API contract／其他限制

## Acceptance criteria
- [ ] ...
- [ ] ...

## Required verification
- `npm run lint`
- `npm run typecheck`
- `npm test -- ...`
- Browser check：...

## Git authorization
- 允許修改檔案：是
- 允許 commit：否
- 允許 push：否
```

若需要 commit 或 push，必須在輸入中另外明確授權。

---

## Frontend Debug

### 何時使用

有可觀察的錯誤、退化、console error、stack trace、測試失敗或 UI 行為不符預期，需要先證明 root cause 再修改時使用。

### 建議附件

- reproduction Markdown
- screenshot／screen recording
- console、network、test 或 stack-trace 文字
- 相關 component／route／test 路徑

### 最小輸入

```text
請調查並修正附件 BUG-123.md 描述的問題。
先重現或取得等價證據，確認 root cause 後才修改；完成後執行能直接覆蓋原始症狀的驗證。
不要做無關重構，也不要 commit 或 push。
```

### 完整輸入模板

```markdown
請執行 Frontend Debug。

## Symptom
<使用者看到的錯誤或異常行為>

## Reproduction
1. ...
2. ...
3. ...

## Expected behavior
<正確行為>

## Evidence
- Error：`...`
- Screenshot：<附件名稱>
- Network／console／test output：<附件或摘要>

## Suspected paths
- `src/...`
- 若猜測錯誤，允許追蹤 definitions/usages：是

## Constraints
- 不修改：`...`
- 不升級 dependency
- 不做無關 refactor

## Verification
- 必須重跑原始 reproduction
- 必須執行：`...`

## Git authorization
- 允許修改檔案：是
- 允許 commit／push：否
```

即使提供了懷疑原因，也應標記為 hypothesis，讓 Agent 以證據驗證，而不是直接照猜測修改。

---

## Frontend Review

使用時必須明確指定一種 mode。

### Staged mode

只 review `git diff --cached`。未 staged、untracked 與 branch history 都不在範圍。

```markdown
請使用 Frontend Review 的 staged mode。

## Scope
- 只檢查：`git diff --cached`
- 排除 unstaged／untracked：是

## Focus
- correctness
- maintainability
- accessibility（如適用）
- security/privacy（如適用）

## Output
只回報具體 findings，附檔案與行號；不要修改檔案，不要提出只有新增 unit test 的建議。
```

### Heavy staged mode

適合風險高、改動大、release 前或需要高冗餘 reviewer quorum 的 staged diff。

```markdown
請使用 Frontend Review 的 heavy staged mode。

## Scope
- 只檢查：`git diff --cached`

## Reason for heavy review
<高風險原因，例如 auth、payment、permission、large refactor>

## Required emphasis
- <特別需要深查的 component／風險>

## Output
維持完整 reviewer quorum 與 validator passes；若無法達成，標示 Incomplete，不要降低標準後宣稱完成。
```

### Branch mode

比較 source branch 相對 target branch 真正引入的 committed contribution。

```markdown
請使用 Frontend Review 的 branch mode。

## Git refs
- Source：`feature/example`
- Target：`master`
- 允許 non-destructive fetch target：是

## Scope
只 review pinned merge-base 到 pinned source SHA 的 committed diff。
排除 index、working tree、untracked files 與 target-only changes。

## Focus
- correctness
- regression risk
- architecture
- security/privacy（如適用）

## Output
回報 source、target、merge-base short SHA、verdict，以及具有檔案與行號的具體 findings。
```

Review Agent 永遠是 read-only；不要要求它順便修正。需要修正時，把 findings 交給 `Frontend Implementation` 或 `Frontend Debug`。

---

## VS Code Skill Creator

### 何時使用

建立新的 Agent Skill、改善既有 Skill 的觸發描述，或用正負 query 評估 routing precision/recall 時使用。

### 建議附件

- 目標 Skill 的初稿或既有 `SKILL.md`
- 必須保留的 references／scripts／templates
- 正向與負向觸發範例

### 最小輸入

```text
請建立一個名為 `<skill-name>` 的 Agent Skill，安裝目標是 `~/.copilot/skills/<skill-name>/`。
用途：<用途>。
先定義正向與負向觸發 query，完成 validation 與 holdout evaluation 後再回報最佳 description。
```

### 完整輸入模板

```markdown
請執行 VS Code Skill Creator。

## Skill identity
- Name：`<lowercase-kebab-case>`
- Target：`~/.copilot/skills/<skill-name>/`
- Purpose：...

## Must trigger for
- ...
- ...

## Must not trigger for
- ...
- ...

## Required resources
- references：...
- scripts：...
- templates：...

## Constraints
- 支援平台：Ubuntu／Windows／macOS
- 不允許：未確認的 CLI、load-time command、credentials
- Provenance／license：...

## Acceptance criteria
- frontmatter validation 通過
- relative resources 可解析
- training 與 holdout query 分離
- 回報 routing errors 與最佳 description
```

---

## 不需要選 Agent 的工作

下列工作直接使用 Agent Skill，比建立或選擇 Custom Agent 更合適：

### 產生 staged commit subject

```text
/frontend-staged-commit-message
```

建議輸入：

```text
/frontend-staged-commit-message
請只根據目前的 git diff --cached 產生至少五個英文 Conventional Commit subjects。
每個選項各占一行，從最簡短的安全描述依序增加到最詳細、但仍受 staged diff 支持的描述。
不要 stage、commit 或修改檔案。
```

其他單次、確定性、沒有特別工具邊界、handoff 或多 worker 編排的工作，也應優先使用 Skill，而不是新增 Agent picker 項目。
