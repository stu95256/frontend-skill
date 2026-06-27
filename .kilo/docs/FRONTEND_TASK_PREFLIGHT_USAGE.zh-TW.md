# FRONTEND_TASK_PREFLIGHT_WORKFLOW 使用說明（Kilo Code）

這份文件是給使用者看的操作指南：當你在 Kilo Code 裡要做前端任務時，如何啟用 `FRONTEND_TASK_PREFLIGHT_WORKFLOW`，以及 prompt 應該怎麼輸入。

## 1. 這個 workflow 是做什麼的？

`FRONTEND_TASK_PREFLIGHT_WORKFLOW` 是「開始寫程式之前」的前期工作流。

它的目標不是立刻改 code，而是先讓 agent 完成：

1. 釐清你的目標。
2. 讀你指定的相關程式碼。
3. 查附近用法、相似元件、測試、route、i18n、shared components。
4. 如果有 Figma / 截圖 / 設計稿，整理設計意圖。
5. 比對 Figma 與現有產品程式碼的落差。
6. 先提出問題、方案與取捨。
7. 如果有需要你回答的問題，用中文提出；程式識別字、路徑、命令、enum value、API 欄位可保留英文。
8. 最後產出 implementation plan。
9. 在 plan 裡明確要求後續生成 code 的 variable / function 名稱不要用簡寫，並保留重要 domain qualifier，例如不要把 `isSpcTableEmptyVal` 縮成 `isEmptyVal`。
10. 等你批准後，才開始實作。

簡單說：

```text
不要一開始就叫 AI 改 code。
先叫 AI 做 preflight，產出計畫。
你確認方向後，再叫 AI 照計畫實作。
```

## 2. 什麼時候應該使用？

遇到以下任務時，建議先用這個 workflow：

- 新增前端功能。
- 修改 UI / layout / styling。
- 根據 Figma 或截圖調整畫面。
- React component 重構。
- TypeScript 型別或 props 設計。
- Tailwind 樣式調整。
- Ant Design 元件使用或客製。
- AG Grid 表格功能或樣式調整。
- react-hook-form 表單與驗證。
- react-i18next 多語系文案。
- react-router-dom route / navigation。
- accessibility / responsive / loading / empty / error state。
- 你不確定 Figma 跟現有產品哪個才是正確來源。

不太需要用的情況：

- 很小的 typo 修正。
- 明確的一行設定修改。
- 你已經有完整計畫，只是要 agent 執行。

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
請使用 frontend-task-preflight skill。
```

更保險的寫法是：

```text
請使用 frontend-task-preflight skill，並遵守 Frontend Preflight Rule。
這次只做 preflight，不要修改程式碼。
```

## 4. 最推薦的 prompt 模板

每次要做前端任務時，可以用這個模板：

```text
請使用 frontend-task-preflight skill。

目標：
[描述你想完成什麼，以及為什麼要做]

相關程式碼：
- [檔案或資料夾路徑 1]
- [檔案或資料夾路徑 2]

Figma / 設計 / 截圖：
- [Figma 連結、截圖、設計描述，沒有就寫「無」]

已知問題或落差：
- [例如：Figma 上按鈕在右邊，但目前產品在左邊]
- [例如：設計稿沒有 loading state，但目前 API 會慢]

限制：
- [例如：不要改 API]
- [例如：不要換 UI library]
- [例如：要保留現有 route]

請先只做 preflight，不要修改程式碼。
請輸出：
1. Intake Summary
2. Code Reconnaissance
3. Design / Figma Reconnaissance，如果適用
4. Gap Matrix，如果 Figma 和現有 code 不一致
5. Clarifying Questions：如需詢問使用者，問題請使用中文；必要的 code identifiers / paths / commands 可保留原文
6. Approach Options
7. Implementation Plan
8. Naming Plan：生成 code 的變數與 function 命名規則，避免簡寫或過度泛化
9. Plan Self-review

等我批准 implementation plan 後，再開始實作。
```

## 5. 最短可用 prompt

如果你不想每次打很長，可以用這個：

```text
請使用 frontend-task-preflight skill。
目標是：[你的任務]
相關檔案：[檔案路徑]
設計參考：[Figma/截圖/無]

只做 preflight，不要改 code。
請先讀相關程式碼，整理 gap matrix、方案選項和 implementation plan。
等我批准後再實作。
```

## 6. 如果有 Figma，怎麼輸入？

有 Figma 時，重點是不要只說「照 Figma 改」。你應該提醒 agent 比對現有 code。

```text
請使用 frontend-task-preflight skill。

目標：
把訂單列表頁調整成 Figma 的新版 layout。

相關程式碼：
- src/pages/orders/OrderListPage.tsx
- src/components/orders/OrderTable.tsx
- src/i18n/locales/zh-TW/orders.json

Figma：
- [貼上 Figma 連結]

已知落差：
- Figma 裡的 filter 區塊在表格上方，但目前產品放在側邊 drawer。
- Figma 沒有 empty state，但目前產品有。
- Figma 的表格欄位比現有產品少。

限制：
- 不要改 API response shape。
- 優先使用現有 Ant Design 與 AG Grid 包裝元件。
- 文案要走 react-i18next。

請只做 preflight，不要修改程式碼。
請比對 Figma 與現有 code，產出 gap matrix。
請提出 2-3 個實作方案與推薦方案。
請在 implementation plan 裡加入 Naming Plan：後續生成 code 的變數與 function 名稱要保留 domain 語意，不要用簡寫或過度泛化名稱，例如不要把 isSpcTableEmptyVal 縮成 isEmptyVal。
最後產出 implementation plan，等我批准後再實作。
```

## 7. 如果沒有 Figma，只是一般功能，怎麼輸入？

```text
請使用 frontend-task-preflight skill。

目標：
在使用者列表頁新增「停用使用者」功能。

相關程式碼：
- src/pages/users/UserListPage.tsx
- src/components/users/UserTable.tsx
- src/api/users.ts

Figma / 設計：
無，請依照現有 UI pattern。

限制：
- 不要新增新的 UI library。
- 優先使用既有 confirm modal pattern。
- 需要考慮 loading、error、成功提示與 i18n。

請只做 preflight，不要修改程式碼。
請先找附近相似功能，再提出 implementation plan。
```

## 8. 如果是 bug，怎麼輸入？

Bug 類任務也可以用 preflight，但要要求 agent 先找 root cause，不要直接猜修法。

```text
請使用 frontend-task-preflight skill。

問題：
會員編輯頁按下儲存後，偶爾會顯示成功訊息，但列表頁資料沒有更新。

相關程式碼：
- src/pages/members/MemberEditPage.tsx
- src/api/members.ts
- src/pages/members/MemberListPage.tsx

限制：
- 先不要修改程式碼。
- 先確認 root cause 和資料流。
- 如果需要改 cache invalidation、navigation 或 API handling，請先在 plan 裡說明。

請只做 preflight。
請輸出：
1. 可能原因列表
2. 需要讀的檔案與實際發現
3. root cause 假設
4. 需要我確認的問題
5. implementation plan
```

## 9. 如果任務很大，怎麼輸入？

任務很大時，要明確要求 agent 拆 scope，不要一次做完。

```text
請使用 frontend-task-preflight skill。

大目標：
重做後台 Dashboard 首頁。

相關範圍：
- src/pages/dashboard/
- src/components/dashboard/
- src/api/dashboard.ts

設計：
- [Figma 連結]

請先只做 preflight，不要實作。
如果範圍太大，請幫我拆成多個階段：
1. 必須先做的基礎改動
2. 可以獨立實作的區塊
3. 需要另外確認的設計或 API 問題
4. 每個階段的驗證方式

最後請給我 phase-based implementation plan。
```

## 10. Kilo 回覆後，我應該怎麼接？

### 情況 A：計畫看起來正確

你可以回：

```text
計畫 OK，請照 implementation plan 開始實作。
請一次完成 Task 1，完成後先停下來回報變更與驗證結果。
```

或：

```text
計畫 OK，請開始實作。
實作時請遵守 plan 中的 file map 和 verification plan。
```

### 情況 B：有些方向要改

你可以回：

```text
先不要實作。
請調整 plan：
1. [你要改的點]
2. [你要保留的限制]
3. [你不同意的方案]

調整後重新輸出 implementation plan。
```

### 情況 C：問題太多，需要先討論

你可以回：

```text
先不要實作。
我先回答 blocking questions：
1. ...
2. ...
3. ...

請根據這些答案更新 gap matrix 和 implementation plan。
```

### 情況 D：只想先做一小部分

```text
先不要做完整計畫。
請只執行 plan 裡的 Task 1。
完成後回報：
- 改了哪些檔案
- 為什麼這樣改
- 跑了哪些驗證
- 是否還有後續 Task
```

## 11. 常見錯誤 prompt

### 錯誤 1：太模糊

```text
幫我照 Figma 改一下頁面。
```

問題：
- 沒有目標。
- 沒有檔案路徑。
- 沒說哪些差異是必須改。
- Agent 可能直接改 code。

改成：

```text
請使用 frontend-task-preflight skill。
目標是讓訂單列表頁的篩選區接近 Figma 設計。
相關檔案是 src/pages/orders/OrderListPage.tsx。
請先比對 Figma 和現有 code，不要直接修改。
請輸出 gap matrix 和 implementation plan。
```

### 錯誤 2：直接要求實作

```text
幫我新增這個功能並改好。
```

如果任務不小，建議改成：

```text
請先使用 frontend-task-preflight skill 做 preflight。
等我批准 plan 後再實作。
```

### 錯誤 3：只相信 Figma

```text
全部照 Figma，現有 code 不重要。
```

除非你真的確定要完全重做，否則建議改成：

```text
請把 Figma 當成設計輸入，但也要比對現有產品行為。
如果 Figma 和現有 code 不一致，請列在 gap matrix，並標出需要我決定的項目。
```

## 12. 你可以固定貼在任務開頭的短句

如果你只想記一句話，記這句：

```text
請使用 frontend-task-preflight skill，只做 preflight，不要改 code；先讀相關程式碼並產出 gap matrix、方案選項與 implementation plan，且在 plan 中要求後續生成 code 的變數/function 名稱不要用簡寫、不要移除重要 domain qualifier，等我批准後再實作。
```

## 13. 完成 preflight 的判斷標準

一個合格的 preflight 結果應該至少包含：

- Agent 有讀你指定的檔案。
- Agent 有找附近 pattern，而不是只看單一檔案。
- 有列出不確定處和需要你決定的問題。
- 有區分 Figma、現有 code、產品需求、假設。
- 有 gap matrix，尤其是 Figma 和現有產品不同時。
- 有 2-3 個方案或至少一個推薦方案與理由。
- implementation plan 有 exact file paths。
- implementation plan 有 Naming Plan，要求生成 code 的 variable / function 名稱保持描述性與 domain-specific，不使用簡寫，也不移除重要 domain qualifier。
- 每個 task 有驗證方式。
- Agent 明確說：等你批准後才實作。

如果缺少這些，你可以要求：

```text
這份 preflight 不完整。請補上：
1. Code Reconnaissance
2. Gap Matrix
3. Approach Options
4. 每個 task 的驗證方式
並且先不要實作。
```
