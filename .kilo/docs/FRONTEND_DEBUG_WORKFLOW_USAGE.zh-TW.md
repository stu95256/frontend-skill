# Frontend Debug Workflow 使用說明

這份文件是給 Kilo Code / coding agent 使用的 prompt template。它對應：

- Skill: `frontend-debug-workflow`
- Rule: `rules/frontend-debug.md`
- Full workflow: `workflows/FRONTEND_DEBUG_WORKFLOW.md`

## 何時使用

當你要我 debug 前端 code，而且會提供一個或多個檔案位置與問題描述時使用。

適合：

- React component 壞掉
- TypeScript / TSX error
- console error
- UI 點擊沒有反應
- route / navigation 問題
- form validation / submit 問題
- AG Grid row / column / render 問題
- Ant Design Form / Table / Modal 問題
- i18n key / interpolation / locale formatting 問題
- Tailwind / responsive / visual behavior 問題

## 建議 prompt

```text
請使用 frontend-debug-workflow skill，並遵守 Frontend Debug Rule。

我要 debug 這些位置與問題：

Files / symbols:
- path/to/file.tsx
- path/to/another-file.ts

Problem:
- 這裡描述錯誤、console message、UI 異常、測試失敗或重現步驟。

Constraints:
- 不要改 API contract / 不要大重構 / 只能改前端 / 保留現有 UX ...

請先讀指定檔案和附近使用方式，找 root cause，選擇應使用的 local frontend skills，寫出最小修正方案，然後開始修正並驗證。
最後請輸出 debug report：files inspected、evidence、root cause、skills used、changes made、verification、remaining risks。
```

## 簡短 prompt

```text
請使用 frontend-debug-workflow debug 並修正：
- 檔案：src/...
- 問題：...
請先查附近使用與 root cause，再選 skill 修正，最後驗證並回報。
```

## Agent 必須做到

1. 先讀指定檔案。
2. 再查附近 usage / call sites / parent components / route / form / grid / i18n / style / API boundary。
3. 先建立 evidence log 與 root cause hypothesis。
4. 再選 exact local skills。
5. 只做最小修正。
6. 修完要跑對應驗證。
7. 最後輸出可回放的 debug report。

## 不要這樣做

- 不要沒讀附近 code 就直接改。
- 不要沒 root cause 就猜修法。
- 不要用 `as any`、eslint disable、空 catch、任意 `setTimeout` 遮掩問題。
- 不要把 unrelated cleanup 混進 debug fix。
- 不要未驗證就說完成。
