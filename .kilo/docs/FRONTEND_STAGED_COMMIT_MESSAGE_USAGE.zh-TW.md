# Frontend Staged Commit Message 使用說明

這份文件是給 Kilo Code / coding agent 使用的 prompt template。它對應：

- Skill: `frontend-staged-commit-message`
- Staging skill path: `.kilo/skills/frontend-staged-commit-message/SKILL.md`

## 何時使用

當你已經 `git add` 前端修改，想要 agent 根據 staged diff 產生一個「單行、英文、精簡」的 commit message 時使用。

適合：

- React / TypeScript / TSX 前端修改
- UI 頁面、component、layout、Tailwind、Ant Design 樣式修改
- AG Grid table / row / column / cell renderer 修改
- react-hook-form 表單行為或 validation 修改
- react-i18next translation key / copy 修改
- react-router-dom route / navigation / query string 修改
- API client / service request / response mapping 修改
- shared hook / formatter / validator / utility 修改

不適合：

- 還沒有 `git add` 任何檔案
- 想根據 unstaged `git diff` 產生 commit
- 想讓 agent 自動 `git add` 或 `git commit`
- 想做 code review；這時請使用 `frontend-staged-review-workflow`
- 想 debug 或修 code；這時請使用 `frontend-debug-workflow`

## 輸出格式

此 skill 預設只輸出一行：

```text
<type>: <concise English frontend change description>
```

重要規則：

- 必須是英文。
- 必須是單行。
- 不要 Markdown code block。
- 不要 body / footer / bullet list。
- 不要 `Co-Authored-By` 或 AI attribution。
- 不要使用 Conventional Commit scope 括號。

不要這樣：

```text
feat(order-list): add bulk selection actions
fix(login): preserve redirect target after sign-in
style(user-profile): align avatar layout
```

要這樣：

```text
feat: add bulk selection actions to order list
fix: preserve login redirect target after sign-in
style: align avatar layout on user profile page
```

## 建議 prompt

```text
請使用 frontend-staged-commit-message skill。

目標：
根據我目前已經 git add 的前端修改，產生一個單行英文 commit message。

限制：
- 只讀取 `git diff --cached`。
- 不要讀取 unstaged `git diff` 作為 commit 內容來源。
- 不要執行 `git add`。
- 不要執行 `git commit`。
- 不要修改檔案。
- 不要跑 format/lint/test/build。
- 輸出必須只有一行英文。
- 格式使用 `feat: ...` / `fix: ...` / `style: ...`，不要使用 `feat(scope): ...`。
- 原本 scope 中的頁面、component、API、module、shared function context，請寫進後面的英文描述。
- 不要輸出 markdown、code block、body、footer、解釋文字或 AI attribution。
```

## 最短可用 prompt

```text
請使用 frontend-staged-commit-message，根據 git diff --cached 產生一個單行英文 commit message。不要使用 scope 括號，格式用 `feat: ...` / `fix: ...` / `style: ...`，不要改檔或 commit。
```

## 使用前檢查

你可以先確認目前是否有 staged files：

```bash
git status --short
git diff --cached --name-only
```

如果 `git diff --cached --name-only` 沒有任何輸出，代表目前沒有 staged changes，skill 會停止並回報沒有 staged 內容。

## Type 選擇提示

| Type | 使用時機 | 範例 |
|---|---|---|
| `feat` | 新增使用者可見功能、UI 行為、API request capability | `feat: add status filter to user management table` |
| `fix` | 修正 bug、edge case、API response handling、state/route/form/table 問題 | `fix: preserve login redirect target after sign-in` |
| `style` | 只改視覺、spacing、layout、CSS、Tailwind、Ant Design styling | `style: refine filter panel spacing on report page` |
| `refactor` | 不改行為的抽 function、搬 shared util、簡化 state mapping | `refactor: extract empty value normalization into shared formatter` |
| `perf` | 減少 re-render、改善 AG Grid / React performance | `perf: reduce user table re-renders during filter changes` |
| `docs` | 只改文件 | `docs: document staged commit message workflow` |
| `test` | 只改測試 | `test: update login redirect coverage` |
| `build` | Vite、bundle、path alias、package scripts、build deps | `build: add Vite path alias resolution` |
| `ci` | CI/CD only | `ci: run frontend typecheck on pull requests` |
| `chore` | 維護、依賴、工具設定，不影響產品行為 | `chore: update frontend lint configuration` |

## 前端 context 要寫進描述

原本 Conventional Commit scope 可能會寫在括號中，但此 skill 要把 context 放到描述內。

例如：

| 變更類型 | 建議輸出 |
|---|---|
| order list 頁面新增批次選取 | `feat: add bulk selection actions to order list` |
| login redirect bug | `fix: preserve login redirect target after sign-in` |
| user profile 頁面 avatar layout | `style: align avatar layout on user profile page` |
| user API request 新增 status filter | `feat: include status filter in user list requests` |
| shared formatter 抽出 empty value normalization | `refactor: extract empty value normalization into shared formatter` |
| AG Grid row identity bug | `fix: stabilize AG Grid row identity in user table` |
| i18n label 缺漏 | `fix: add missing user table translation labels` |

## 如果 staged changes 混了多個不同意圖

如果 staged changes 看起來應拆成多個 commit，agent 應先提醒你，例如：

```text
The staged changes look like separate commits:
- fix: preserve login redirect target after sign-in
- style: refine dashboard card spacing
```

若你明確要求「還是給一行」，agent 才選主要意圖產生單行 commit message，並避免過度宣稱。

## 和其他 workflow 的差異

| Skill / Workflow | 使用時機 | 是否修改 code | 主要輸出 |
|---|---|---|---|
| `frontend-staged-commit-message` | 已 `git add`，只想產生單行英文 commit message | 不修改 | one-line commit message |
| `frontend-staged-review-workflow` | 已 `git add`，想 review staged diff | 不修改 | staged diff review report |
| `frontend-debug-workflow` | 有 bug / error / UI 異常，想查 root cause 並修正 | 會修改 | debug report + fix |
| `frontend-task-preflight` | 開始實作前要釐清需求和計畫 | 不修改 | implementation plan |
