# 前端 Debug Workflow

最後更新：2026-05-30

本文件整理一套專門用於「debug 使用者指定的前端程式碼與問題」的 workflow。使用者會提供一段或多段程式碼位置，以及看到的錯誤、異常行為、截圖、console output、測試失敗或重現描述。Agent 必須先查看相關檔案與附近使用方式，理解為什麼會發生問題，再選擇正確的 local skills 修正，最後驗證並紀錄整個 debug workflow。

適用技術棧：React、TypeScript、Tailwind、AG Grid React、Ant Design、react-i18next、react-router-dom、react-hook-form，以及 browser-visible frontend behavior。

---

## 1. 來源與參考

| 類別 | 來源 | 可採用重點 |
|---|---|---|
| Claude Code common workflows | https://docs.anthropic.com/en/docs/claude-code/common-workflows | Debug / explore 類任務要先理解 codebase 與 execution flow；可先問 code 如何運作，再追蹤前後端或 UI 流程。 |
| Claude Code subagents | https://docs.anthropic.com/en/docs/claude-code/sub-agents | 複雜 debug 可委派 read-only investigation sub-agent，但主 agent 必須整合證據與負責修正。 |
| Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | Workflow 適合可預測流程；用 prompt chaining / evaluator-optimizer 思維設中間 gate，避免沒有證據就進入下一步。 |
| Superpowers systematic-debugging | https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md | 核心原則：No fixes without root cause investigation；先讀錯誤、重現、查近期變更、追資料流，再修 root cause。 |
| Chrome DevTools JavaScript debugging | https://developer.chrome.com/docs/devtools/javascript/ | Debug 基本流程：reproduce the bug、pause with breakpoints、step through code、inspect values、fix and verify。 |
| Chrome DevTools Console logging | https://developer.chrome.com/docs/devtools/console/log | Console / warning / error 是 evidence；需要記錄實際訊息與觸發步驟，不可只憑印象修。 |
| Playwright trace viewer | https://playwright.dev/docs/trace-viewer | 對 browser / E2E 問題，可用 trace、screenshots、DOM snapshots、network/action timeline 回放問題。 |
| React Developer Tools | https://react.dev/learn/react-developer-tools | React 問題可用 component tree / props / state / hook 狀態輔助確認 render 與 state flow。 |

---

## 2. 核心原則

1. **先 root cause，再修正。**
   - 沒有完成 evidence gathering / reproduction / code path tracing 前，不提出或套用修法。
   - 不做「看起來可能」的猜測式修改。

2. **使用者給的路徑只是起點，不是完整範圍。**
   - 必須讀指定檔案內容。
   - 必須查附近使用方式：imports、call sites、parent components、routes、hooks、store、API client、i18n keys、form schema、grid column defs、style/token 來源。
   - 若問題跨多檔，建立 data/control flow map。

3. **每個重要判斷都要有 evidence。**
   - Evidence 可以是 error message、stack trace、reproduction command、console output、test failure、git diff、source line、附近 working example、官方文件、browser observation。
   - 最終報告要保留 debug log，不只說「已修好」。

4. **依問題類型選 skill，而不是固定套同一套技能。**
   - React hook 問題、router 問題、form 問題、AG Grid 問題、AntD 問題、Tailwind / responsive 問題、i18n 問題、browser behavior 問題要選不同 local skills。
   - 只能引用本專案存在的 `skills/<skill-name>/SKILL.md`。

5. **修正要最小化且可驗證。**
   - 一次只修 root cause，不順手重構。
   - 修完要跑與問題對應的 verification：typecheck、lint、test、targeted reproduction、browser check 或 manual checklist。

6. **debug workflow 需要紀錄開始、過程、完成。**
   - Intake、evidence、hypothesis、selected skills、fix plan、changed files、verification result、remaining risk 都要可回放。

---

## 3. Workflow 總覽

```text
[0 Intake problem packet]
  -> [1 Read specified code + nearby usage]
  -> [2 Reproduce / gather evidence]
  -> [3 Trace data/control/render flow]
  -> [4 Root cause hypothesis gate]
  -> [5 Select local skills for the fix]
  -> [6 Minimal fix plan]
  -> [7 Implement root-cause fix]
  -> [8 Verify]
  -> [9 Debug record + completion report]
```

建議 gate：

| Gate | 何時發生 | 通過條件 | 未通過時 |
|---|---|---|---|
| Intake Gate | Step 0 後 | 至少知道問題描述與一個檔案 / symbol / route / component / error 訊息 | 若完全無法定位，先問 1-3 個 blocking questions；否則標假設後搜尋。 |
| Evidence Gate | Step 2 後 | 有錯誤訊息、重現方式、測試失敗、browser observation 或可解釋的 source evidence | 補查 logs、跑 command、讀更多檔、派 read-only investigator。 |
| Root Cause Gate | Step 4 後 | 能清楚說出「因為 X，在 Y 條件下導致 Z」並指到 source lines / call path | 不修；回 Step 1-3 追資料流或查 working example。 |
| Skill Gate | Step 5 後 | 列出 exact local skills、選用原因、對應問題類型；所有 skill path 存在 | 移除不存在的 skill；用可用替代 skill 或記錄 missing gap。 |
| Fix Gate | Step 6 後 | 最小修正方案只針對 root cause；列出要改的 exact files | 若需要架構決策或 scope 擴大，先向使用者回報。 |
| Verification Gate | Step 8 後 | 有 command / browser / manual evidence 證明問題改善，且無明顯 regression | 若失敗，最多回到 hypothesis loop；不要疊加隨機修法。 |
| Completion Gate | Step 9 後 | Debug record 完整，包含 changed files、verification、剩餘風險 | 補紀錄或揭露未完成項目。 |

---

## 4. Step-by-step Workflow

### Step 0：Intake problem packet

使用者可能提供：

- 一個或多個路徑：`src/components/UserTable.tsx`、`src/routes/users.tsx`。
- 一段錯誤描述：console error、TypeScript error、UI 異常、點擊後沒有反應、資料沒有更新。
- Stack trace、截圖、測試失敗、重現步驟。
- 限制：不要改 API、不要改樣式、只改某個元件、需要保留既有 UX。

輸出 / 內部紀錄：

```markdown
## Debug Intake

**Problem statement:**
- ...

**User-provided code references:**
- `path/to/file.tsx`

**Observed symptoms / errors:**
- ...

**Known reproduction steps:**
1. ...

**Constraints:**
- ...

**Initial assumptions:**
- ...

**Blocking missing info:**
- ...
```

如果使用者只給模糊描述但有路徑，先讀檔和搜尋，不要立刻問問題。只有完全無法定位或下一步工具行動會大幅不同時才問。

### Step 1：讀指定程式碼與附近使用

必做：

1. 讀使用者指定檔案。
2. 讀錯誤行號附近上下文。
3. 搜尋該 component / hook / function / route / form / grid config 的使用處。
4. 讀 import/export 相關檔案。
5. 找同專案中類似且正常運作的 pattern。

建議 commands / tools：

```bash
git status --short --branch
git diff -- path/to/file.tsx
git log --oneline -10 -- path/to/file.tsx
```

使用 file search：

```text
search_files("ComponentName", path="src")
search_files("useProblemHook", path="src")
search_files("translation.key", path="src")
search_files("route-id-or-path", path="src")
```

附近使用檢查表：

| 問題類型 | 附近要查什麼 |
|---|---|
| React component | parent props、child callbacks、state owner、memoization、conditional render、key。 |
| `useEffect` / async | dependency array、cleanup、stale closure、race condition、derived state、subscription lifecycle。 |
| TypeScript | inferred type、generic boundary、unsafe assertion、nullable state、API response type、tsconfig strictness。 |
| Router | route definition、loader/action、navigation call、params、query string、error boundary。 |
| Form | default values、resolver/schema、controlled/uncontrolled fields、field array、submit handler、server errors。 |
| AG Grid | rowData identity、columnDefs memoization、valueGetter/cellRenderer、row id、server-side model、grid API timing。 |
| Ant Design | component API、controlled value、Form.Item name/valuePropName、Modal lifecycle、Table rowKey、theme tokens。 |
| i18n | namespace、key existence、interpolation、fallback language、date/number formatting、long-string layout。 |
| Tailwind / responsive | class conflict、breakpoint order、container width、theme token、dark mode / CSS variable。 |
| Browser behavior | console errors、network response、DOM state、event listener, focus, pointer/keyboard interaction。 |

### Step 2：重現與收集 evidence

優先順序：

1. 如果有 test command / typecheck / lint 可重現，先跑最小 command。
2. 如果是 browser-visible 問題，用 Playwright / DevTools / screenshot / console / network 收 evidence。
3. 如果無法重現，仍要從 source trace 與附近 working pattern 建立可檢驗假設，但要標記未完全重現。

Evidence record：

```markdown
## Evidence Log

| Evidence ID | Source | Command / File / Observation | Result | Meaning |
|---|---|---|---|---|
| E1 | terminal | `npm run typecheck` | `TS2322 at src/...` | Type mismatch confirms ... |
| E2 | source | `src/...:42-55` | `useEffect` depends on stale value | Likely root cause ... |
| E3 | browser | Console error after click | `Cannot read properties of undefined` | Runtime path ... |
```

### Step 3：追 data / control / render flow

Trace 要回答：

- 壞掉的值從哪裡來？
- 哪個 component / hook / route / form / grid API 傳遞它？
- 哪個條件讓它變錯？
- 正常 pattern 在同專案中如何處理？
- 這是 source bug、state ownership bug、effect lifecycle bug、type bug、API contract bug、UI library usage bug，還是 verification/test setup bug？

Flow map 模板：

```markdown
## Flow Map

1. `src/api/users.ts:getUsers()` returns ...
2. `src/routes/users.tsx` loader maps ...
3. `src/components/UserTable.tsx` receives `rows` ...
4. `columnDefs` cellRenderer expects ...
5. Failure occurs when ... because ...
```

### Step 4：Root cause hypothesis gate

進入修正前必須寫出單一主假設：

```markdown
## Root Cause Hypothesis

I think the root cause is: ...

Because:
- E1 shows ...
- `path/file.tsx:line` does ...
- Similar working code in `path/working.tsx` handles it by ...

What would disprove this:
- If ... then this hypothesis is wrong.
```

不可接受：

- 「可能是 state 問題，所以改一下」。
- 「看起來像型別錯，所以加 `as any`」。
- 「先試試看」。
- 同時提出 3 個沒有 evidence 的修法。

### Step 5：選擇應使用的 local skills

所有選用 skill 必須存在於 `skills/<skill-name>/SKILL.md`。選 skill 的結果要寫進 debug record。

| 問題 / evidence | 應使用 skill（exact local names） | 使用目的 |
|---|---|---|
| 任何 bug / unexpected behavior / failing test | `systematic-debugging` | 強制 root cause first、重現、trace flow、hypothesis gate。 |
| 需要小步修正避免擴大 scope | `incremental-implementation` | 最小修正、分步驗證。 |
| 修完前需要驗證完成標準 | `verification-before-completion` | 防止未驗證就宣稱完成。 |
| 需要依官方文件或 source 決定 API 用法 | `source-driven-development` | 查官方 docs / source，避免猜 API。 |
| React component / props / hooks / state | `react-dev`、`react-state-management` | React component/state pattern 修正。 |
| `useEffect` / cleanup / stale closure / async effect | `react-useeffect` | Effect lifecycle 與依賴修正。 |
| TypeScript type / TSX / generics / unsafe assertion | `typescript-advanced-types`、`typescript-code-reviewer` | 型別設計與 unsafe TypeScript 修正。 |
| Router / route params / navigation / loaders/actions | `react-router-declarative-mode`、`react-router-data-mode`、`react-router-framework-mode` | 依專案 routing mode 選用。 |
| Ant Design / Antd component behavior | `ant-design`、`antd` | AntD API、Form/Table/Modal、theme/token。 |
| AG Grid behavior / rendering / data update | `ag-grid` | Grid API、row identity、column defs、performance。 |
| React Hook Form / validation / submit | `react-hook-form-zod` | Form state、schema、errors、controlled/uncontrolled。 |
| i18n / react-i18next / missing text | `internationalization-i18n` | namespace/key/interpolation/locale formatting。 |
| Tailwind / responsive / design tokens | `tailwind-design-system`、`tailwind-v4-shadcn`、`responsive-design` | class/token/responsive 修正。 |
| Accessibility / keyboard / focus | `accessibility-compliance` | a11y root cause 與修正。 |
| Browser-visible runtime issue | `browser-testing-with-devtools`、`webapp-testing` | Browser verification、console/network/DOM。 |
| Playwright trace / E2E reproduction | `playwright-best-practices` | Trace viewer、selector/action/debug pattern。 |
| Performance / excessive renders / expensive UI | `performance-optimization`、`vercel-react-best-practices` | 前端效能與 render behavior。 |
| Security / privacy bug | `security-and-hardening`、`secpriv-code-review` | 安全與 privacy 修正。 |

Skill selection record：

```markdown
## Selected Skills

| Skill | Path | Why selected | How it affects the fix |
|---|---|---|---|
| `systematic-debugging` | `skills/systematic-debugging/SKILL.md` | Bug report with reproducible symptom | Root cause gate before edits |
| `react-useeffect` | `skills/react-useeffect/SKILL.md` | Evidence points to stale closure | Fix effect dependencies / cleanup |
```

### Step 6：最小修正方案

修正前寫出：

```markdown
## Minimal Fix Plan

**Root cause to fix:**
- ...

**Files to change:**
- `path/to/file.tsx` — why

**Exact intended changes:**
1. ...
2. ...

**Verification:**
- `npm run typecheck`
- `npm run lint`
- `npm test -- ...`
- browser reproduction steps / Playwright command

**Out of scope:**
- unrelated refactor
- cosmetic cleanup
- unrelated tests
```

若修正會大幅改架構、改 API contract、改 UX 決策，先回報使用者，不要自行擴大範圍。

### Step 7：開始修正

執行規則：

1. 只改 Step 6 列出的檔案，除非修正過程證明需要新增檔案；新增原因要記錄。
2. 優先使用 `patch` 做精準修改。
3. 不用 `as any`、disable eslint、吞錯、magic timeout 當作根因修正，除非 evidence 證明這正是正確 API usage，且要寫明原因。
4. 一次只修一個 hypothesis。
5. 若修正失敗，回 Step 3 / Step 4，不要疊加隨機修法。

### Step 8：驗證

驗證要對應原問題，不是只跑一個 unrelated command。

| 問題類型 | 最低驗證 |
|---|---|
| TypeScript error | targeted typecheck 或全專案 typecheck。 |
| lint / formatting | targeted lint 或全專案 lint。 |
| test failure | 原本 failing test command 需通過。 |
| browser runtime | 原重現步驟需不再出錯；記錄 console/network/DOM result。 |
| form / table / route / i18n | 對應 user flow 或 component behavior 需驗證。 |
| visual/responsive | 指定 breakpoint / state 需檢查；若只能人工，列 manual checklist。 |

Verification record：

```markdown
## Verification Results

| Check | Command / Steps | Result | Notes |
|---|---|---|---|
| Typecheck | `npm run typecheck` | pass | ... |
| Reproduction | Click ... | pass | Console has no new error |
```

### Step 9：Debug record + completion report

最後輸出要包含：

```markdown
## Frontend Debug Report

### Problem
- ...

### Files inspected
- `...`

### Evidence
- E1: ...
- E2: ...

### Root cause
- ...

### Skills used
- `systematic-debugging` — ...
- `react-useeffect` — ...

### Changes made
- `path/file.tsx`: ...

### Verification
- `npm run typecheck`: pass/fail/skipped with reason
- Reproduction: pass/fail/skipped with reason

### Remaining risks / follow-up
- ...
```

如果無法完成，不能說完成；要輸出 degraded report：已查證內容、阻塞點、需要使用者提供什麼、下一步建議。

---

## 5. Sub-agent 使用規則

一般 debug 優先由主 agent 完成。只有以下情況才派 sub-agent：

- 問題跨很多檔或多個候選 root cause。
- 需要平行查官方文件與 codebase pattern。
- 需要獨立 reviewer 檢查 root cause hypothesis 或 fix plan。

Sub-agent 必須是 read-only investigator，除非主 agent 明確將已確認的 fix plan 拆給 implementation sub-agent。主 agent 仍要驗證結果。

Read-only investigator prompt 需包含：

```text
Follow frontend-debug-workflow and systematic-debugging.
Read the specified files and nearby usage.
Find evidence and root cause hypothesis only.
Do not modify files.
Return: files inspected, evidence, likely root cause, disconfirming evidence, relevant local skills.
```

---

## 6. Common pitfalls

1. 只讀使用者指定檔，沒有查 call sites / parent component / route / hook。
2. 沒重現就修。
3. 把 symptom 當 root cause，例如只加 optional chaining 隱藏錯誤。
4. 用 `as any`、eslint disable、空 catch、setTimeout 當作萬用修法。
5. 沒確認 routing mode 就套錯 React Router skill。
6. AntD Form / Table 問題沒查 controlled props、`name`、`rowKey`、`valuePropName`。
7. AG Grid 問題沒查 row identity、columnDefs memoization、grid API lifecycle。
8. i18n 問題只改顯示文字，沒查 namespace / interpolation / fallback。
9. 修完只說「應該可以」，沒有跑 command 或記錄 manual/browser verification。
10. 修正失敗後繼續疊加第二、第三個猜測，沒有回 root cause gate。

---

## 7. Completion Criteria

Workflow 完成必須滿足：

1. 使用者提供的每個 relevant path / symptom 都被納入 intake。
2. 指定檔案與附近使用已讀取或明確說明無法讀取。
3. Evidence log 至少包含一項可追溯 evidence。
4. Root cause hypothesis 清楚描述 why。
5. Selected skills 使用 exact local skill names，且 path 存在。
6. Fix plan 是最小修正，不包含 unrelated cleanup。
7. 修改已完成或明確標記 blocked / degraded。
8. Verification 結果已記錄。
9. Final debug report 包含 files inspected、root cause、skills used、changes made、verification、remaining risks。
