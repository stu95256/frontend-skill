# 前端任務前期 Workflow 調查與草案

最後更新：2026-05-29

本文件整理一套「任務前期 workflow」，目標是在開始寫程式前，先把使用者目標、相關程式碼、Figma/設計稿、現有前端實作落差、需要補問的細節、應使用的 skills、外部文件與 implementation plan 全部釐清。之後可把本文件濃縮成一個可重複使用的 `SKILL.md`。

本 workflow 特別針對本專案關注的前端技術棧：React、TypeScript、Tailwind、AG Grid React、Ant Design、react-i18next、react-router-dom、react-hook-form。

---

## 1. 來源與參考

| 類別 | 來源 | 可採用重點 |
|---|---|---|
| Claude Code workflow | https://code.claude.com/docs/en/best-practices.md | 採用「explore first, then plan, then code」；大任務先訪談使用者、寫 self-contained spec，再規劃。 |
| Claude Code common workflows | https://code.claude.com/docs/en/common-workflows.md | 使用 plan-before-editing；大型 codebase exploration 可委派 subagent，避免主 context 被搜尋結果污染。 |
| Claude Code plan mode | https://code.claude.com/docs/en/permission-modes.md | Planning 階段只研究、讀檔、寫計畫，不做 source edits；使用者可繼續要求修 plan。 |
| Claude Code subagents | https://code.claude.com/docs/en/sub-agents.md | Subagent 適合 read-only exploration、verbose research、獨立任務；主 agent 必須明確提供 context。 |
| Claude Code skills | https://code.claude.com/docs/en/skills.md | Skill 適合封裝 reusable checklist / workflow；用 progressive disclosure 控制 context。 |
| Anthropic Agent Skills | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md | Skill 是可重用能力包；metadata 決定何時載入，內容應精簡、可操作。 |
| Anthropic skill best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md | 重要規則放前面；fragile workflow 要給明確步驟；大型內容拆到 references。 |
| Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | Workflow 適合可預測流程；用 prompt chaining 與 evaluator-optimizer pattern 做中間 gate 與 plan review。 |
| Superpowers | https://github.com/obra/superpowers | 前期先 brainstorming / spec / planning，使用者 approve 後才實作；plan 要能讓沒有上下文的人照做。 |
| Superpowers brainstorming | https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md | 探索 project context、問澄清問題、提出多方案、取得設計確認、做 spec self-review。 |
| Superpowers writing-plans | https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md | Plan 需 exact files、完整步驟、驗證命令；禁止 TBD/TODO/模糊敘述。 |
| Superpowers subagent-driven-development | https://raw.githubusercontent.com/obra/superpowers/main/skills/subagent-driven-development/SKILL.md | 實作期可 fresh subagent per task + spec review + quality review；本文件只涵蓋實作前期。 |
| Figma Dev Mode | https://www.figma.com/dev-mode/ | Figma 是設計輸入來源，可萃取 layout、tokens、component、interaction，但不是唯一真相。 |
| Figma Dev Mode guide | https://help.figma.com/hc/en-us/articles/15023124644247-Guide-to-Dev-Mode | Dev Mode 可用於工程交付與 inspect，但仍需和 code/design system 對照。 |
| Figma Code Connect | https://developers.figma.com/docs/code-connect/ | 可建立 Figma component 與 code component 的對應；適合檢查設計稿與實作是否有 mapping。 |
| Figma variables | https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma | 變數 / tokens 應對照 Tailwind theme、AntD token、專案 design tokens。 |
| Design Tokens CG | https://www.designtokens.org/tr/drafts/format/ | Token naming / format 可作為跨 Figma 與程式碼的對照參考。 |
| WCAG Quick Reference | https://www.w3.org/WAI/WCAG22/quickref/ | UI planning 階段就要列入 accessibility 驗證，不應最後補救。 |
| WAI-ARIA APG | https://www.w3.org/WAI/ARIA/apg/ | 複雜互動元件需確認 keyboard 與 ARIA pattern。 |
| Tailwind responsive design | https://tailwindcss.com/docs/responsive-design | Responsive plan 要定義 breakpoint 與 layout 行為，而非只照某個截圖尺寸。 |
| Tailwind theme | https://tailwindcss.com/docs/theme | 樣式應優先映射到 theme token，避免任意 magic values。 |
| Ant Design theme | https://ant.design/docs/react/customize-theme | AntD UI 應先查 component/token 能否支援，不要直接硬刻 CSS。 |
| AG Grid accessibility | https://www.ag-grid.com/react-data-grid/accessibility/ | 表格任務要先確認 keyboard、ARIA、screen reader、large data 行為。 |
| AG Grid theming | https://www.ag-grid.com/react-data-grid/theming/ | 表格視覺需對照 AG Grid theme，而非只改局部樣式。 |
| React Hook Form accessibility | https://react-hook-form.com/advanced-usage#AccessibilityA11y | 表單任務要規劃 validation、aria-invalid、role alert、error message mapping。 |
| react-i18next | https://react.i18next.com/ | 文案與錯誤訊息需在計畫階段納入 i18n key、插值、長字串影響。 |

---

## 2. 核心原則

1. 前期 workflow 不寫 code、不修改檔案、不 scaffold。
   - 只做讀檔、搜尋、分析、討論、規劃、文件紀錄。
   - 只有使用者明確批准 plan 並要求開始實作後，才切換到 implementation workflow。

2. Figma 是輸入，不是唯一真相。
   - 需求來源要分成：使用者目標、現有 code、design system、Figma、外部官方文件、討論決策。
   - 當 Figma 與現有實作不同，不直接判斷誰對誰錯，要先做 gap matrix。

3. 先查可查資料，再問使用者。
   - 能從指定檔案、附近用法、官方文件查到的資訊先查。
   - 只問會影響方向、架構、範圍、資料流、UX、a11y、驗證方式的問題。
   - 需要詢問使用者時，問題必須使用中文（預設繁體中文）；程式識別字、路徑、命令、enum value、API 欄位與引用原文可保留英文。

4. Brainstorming 是前期 workflow 的核心，不是 optional。
   - 在寫 implementation plan 前，必須先完成「理解目標 → 找未知 → 提出 2-3 個方案 → 討論取捨 → 收斂設計」這段思考。
   - Brainstorming 的產物不是 code，而是決策、假設、替代方案、取捨理由、設計方向。
   - 如果任務是 bug / feasibility / UI design，brainstorming 要和對應思考 skill 搭配，而不是被 plan 取代。

5. 善用 sub-agent，但主 agent 必須當 coordinator。
   - Sub-agent 做 read-only reconnaissance / web research / plan critique。
   - 主 agent 負責合併結果、辨識衝突、和使用者討論、最後產出 plan。

6. Plan 必須可執行、可驗證、可交接。
   - 包含 exact paths、task order、驗證命令、expected outcome、風險、open questions。
   - 禁止 `TBD`、`TODO`、`handle edge cases`、`write tests` 這類沒有細節的 placeholder。

---

## 3. Workflow 總覽

```text
[0 Intake]
  -> [0.5 Brainstorming / problem framing]
  -> [1 Skill selection]
  -> [2 Codebase reconnaissance]
  -> [3 Figma/design reconnaissance]
  -> [4 Gap analysis]
  -> [5 Unknowns + clarifying questions]
  -> [6 External research]
  -> [7 Approach options]
  -> [8 User discussion / decision]
  -> [9 Implementation plan]
  -> [10 Plan self-review]
  -> [11 Plan review subagent]
  -> [12 Final plan + handoff]
```

建議 gate：

| Gate | 何時發生 | 通過條件 | 未通過時 |
|---|---|---|---|
| Intake Gate | Step 0 後 | 目標、已知檔案、Figma/設計資訊、限制至少有初始描述 | 先補問最基本資訊，或標記假設後只做可行的探索 |
| Brainstorming Gate | Step 0.5 / Step 7 後 | 已理解目標、列出未知、提出替代方案與推薦方向 | 不寫 plan；繼續問問題、補探索或拆小任務 |
| Evidence Gate | Step 4 後 | 每個重要判斷都有 code/Figma/docs/user evidence | 補查檔案、派 subagent、或列為 open question |
| Decision Gate | Step 8 後 | 方向、取捨、blocking questions 已由使用者確認 | 繼續討論，不進入 plan finalization |
| Plan Completeness Gate | Step 10/11 後 | plan 無 placeholder、路徑正確、驗證完整、風險列明 | 修 plan 或補研究 |
| Handoff Gate | Step 12 後 | 使用者批准 plan 或明確要求執行 | 停在 planning，不寫 code |

---

## 4. Step-by-step Workflow

### Step 0：任務 intake

使用者可能提供：
- 目標：要完成什麼、為什麼要做。
- 相關程式碼檔案或目錄。
- 前端 Figma / 截圖 / prototype / design note。
- 已知限制：不能改的行為、deadline、技術限制、API 限制。
- 已知落差：Figma 和實際使用不同的地方。

輸出一份 intake summary：

```markdown
## Intake Summary

**Goal:**

**Known code references:**
- `path/to/file.tsx`

**Design references:**
- Figma: ...
- Screenshot: ...

**Known differences between Figma and product:**
- ...

**Constraints:**
- ...

**Initial assumptions:**
- ...

**Blocking missing info:**
- ...
```

Gate：如果目標或目標檔案完全不明，先問 1-3 個 blocking questions；如果只是細節不明，先標假設並進入探索。

### Step 0.5：Brainstorming / problem framing

這一步是把「使用者給的任務資訊」轉成「可討論、可決策、可規劃的問題」。它應該發生在正式寫 plan 之前，並且在 code / design reconnaissance 後再回來補一輪。

Brainstorming 要回答：
- 使用者真正要達成的結果是什麼，而不是只改某個檔案或照某張圖。
- 哪些資訊是已知事實，哪些只是推測。
- Figma、現有 code、design system、產品行為之間可能有哪些衝突。
- 這個任務可拆成哪些子問題；是否太大，需要先拆 scope。
- 至少 2-3 個可行方向是什麼；各自 tradeoff 是什麼。
- 推薦方向是什麼，以及為什麼。

Brainstorming artifact：

```markdown
## Brainstorming Notes

**User intent:**
- ...

**Known facts:**
- ...

**Assumptions:**
- ...

**Unknowns / risks:**
- ...

**Possible approaches:**
1. ...
2. ...
3. ...

**Recommendation:**
- ...

**Needs user decision before planning:**
- ...
```

和其他思考 skill 的搭配：

| 情境 | 優先思考 skill | 用法 |
|---|---|---|
| 新功能 / UI 改版 / 元件設計 | `brainstorming` | 先理解意圖、問問題、提出 2-3 方案、取得設計方向確認。 |
| 技術可行性不確定 | `spec-driven-development`、`source-driven-development`、`planning-and-task-breakdown` | 先用 spec / source research 把未知拆成可驗證問題；本專案目前沒有 `spike` local skill，不引用不存在的 skill。若之後需要 throwaway prototype workflow，再用 `writing-skills` / `skill-creator` 新增 `spike`。 |
| Bug / 行為異常 / 測試失敗 | `systematic-debugging` | 先找 root cause、重現、比對 working pattern，不要直接猜修法。 |
| 已有方向，需要落成任務 | `writing-plans` | 把已確認的設計轉成 exact files、steps、verification。 |
| 計畫很複雜或風險高 | plan-review subagent | 用 evaluator-optimizer pattern 找缺口、模糊點、scope creep。 |

Gate：如果 brainstorming 還沒有產出推薦方向與待決策問題，不要進入 implementation plan。

### Step 1：判斷應使用哪些 skills

先掃描任務類型，再載入對應 skill。不要寫泛稱「某某 skill/resources」；必須對應到本專案 `skills/<skill-name>/SKILL.md` 內實際存在的 skill。如果需要的 skill 不存在，要在 Skill Selection 中標成 missing，不可假裝已可用。

Local skill matrix：

| 任務類型 / 偵測線索 | 應使用 skill（exact local names） | 使用階段 |
|---|---|---|
| 任何新功能、UI 改版、元件設計、需求仍模糊 | `brainstorming` | Step 0.5 problem framing / 方案討論 |
| 需求要正式化成 spec | `spec-driven-development` | Step 0.5 / Step 5 / Step 7 |
| 需要讀 source 才能確認方向 | `source-driven-development`、`context-engineering` | Step 2 code reconnaissance |
| 技術可行性不確定，但尚未有 local spike skill | `spec-driven-development`、`source-driven-development`、`planning-and-task-breakdown` | Step 0.5 / Step 6；若要 throwaway prototype，先用 `writing-skills` / `skill-creator` 建立 `spike` skill |
| 需要網路搜尋、官方文件查詢，或一般 web search / extraction 被阻擋 | `playwright-mcp-usage` | Step 6 external research；使用 Playwright MCP 真實瀏覽器流程做 DOM / screenshot 查證 |
| 要把已確認方向拆成工作 | `planning-and-task-breakdown`、`writing-plans` | Step 8 implementation plan |
| 後續要交給 sub-agent 實作 | `subagent-driven-development` | Implementation phase handoff |
| Bug、行為異常、測試失敗 | `systematic-debugging` | Step 0.5 / Step 2，先找 root cause 再 plan |
| React component / hooks / props / events | `react-dev`、`react-useeffect`、`react-state-management` | Step 2 / Step 8 |
| TypeScript type design 或 TSX review | `typescript-advanced-types`、`typescript-code-reviewer` | Step 2 / Step 9 / implementation review |
| React Router | `react-router-declarative-mode`、`react-router-data-mode`、`react-router-framework-mode` | Step 2 先判斷 routing mode；Step 8 規劃 route 變更 |
| Ant Design / antd component | `ant-design`、`antd` | Step 3 design mapping / Step 6 docs research / Step 8 UI plan |
| AG Grid React table | `ag-grid` | Step 2 table pattern / Step 3 table states / Step 8 table plan |
| React Hook Form / form validation | `react-hook-form-zod` | Step 2 form pattern / Step 8 validation plan |
| i18n / react-i18next / copy / locale formatting | `internationalization-i18n` | Step 2 i18n key reconnaissance / Step 8 i18n plan |
| Tailwind / design tokens / design system | `tailwind-design-system`、`design-system-patterns`、`design-system-starter` | Step 3 design/token mapping |
| Responsive layout | `responsive-design` | Step 3 responsive analysis / Step 8 responsive plan |
| Accessibility / keyboard / ARIA / contrast | `accessibility-compliance`、`web-design-guidelines` | Step 3 / Step 8 / Step 9 |
| Production UI quality | `frontend-design`、`frontend-ui-engineering`、`web-design-guidelines` | Step 3 / Step 7 / Step 8 |
| Unit / integration tests | `vitest-testing`、`javascript-testing-patterns` | Step 8 test plan |
| E2E / visual / browser QA | `playwright-best-practices`、`webapp-testing`、`browser-testing-with-devtools`、`e2e-testing-patterns` | Step 8 QA plan / implementation verification |
| QA test cases / regression checklist | `qa-test-planner` | Step 8 / Step 9 |
| 完成前驗證 | `verification-before-completion` | Step 9 / Step 12 handoff |
| 之後把本 workflow 寫成 skill | `writing-skills`、`skill-creator` | Future skill authoring |

`spike` 處理規則：本專案目前沒有 `skills/spike/SKILL.md`，所以 workflow 不應把 `spike` 列為可直接使用的 local skill。若未來需要「throwaway experiments」能力，先用 `writing-skills` / `skill-creator` 建立並驗證 `spike` skill；在此之前，用 `spec-driven-development`、`source-driven-development`、`planning-and-task-breakdown` 來處理可行性未知。

Skill selector subagent prompt 模板：

```text
你是 skill selector subagent。不要修改檔案。

Task goal:
[使用者目標]

Known stack / clues:
[React, TypeScript, Tailwind, AG Grid, Ant Design, react-i18next, react-router-dom, react-hook-form, Figma gaps, bug/feature/test 等]

Available local skill matrix:
[貼上或摘要本節 local skill matrix]

Check:
1. Which exact local skills should be loaded now?
2. Which exact local skills should be used by code reconnaissance?
3. Which exact local skills should be used by design/Figma analysis?
4. Which exact local skills should be reserved for implementation or review phase?
5. If external web research is needed, is `playwright-mcp-usage` included and available?
6. Are any referenced skills missing from `skills/<name>/SKILL.md`?

Return:
- Must load now:
- Use during reconnaissance:
- Use during design/Figma analysis:
- Use during web research:
- Use during planning:
- Use during implementation/review later:
- Missing referenced skills:
```

輸出：

```markdown
## Skill Selection

**Must load now:**
- `brainstorming`: because ...

**Use during reconnaissance:**
- `react-dev`: because ...
- `ag-grid`: because ...

**Use during design/Figma analysis:**
- `frontend-ui-engineering`: because ...
- `responsive-design`: because ...

**Use during web research:**
- `playwright-mcp-usage`: because any external web lookup must use Playwright MCP when normal web search / extraction is blocked.

**Use during planning:**
- `planning-and-task-breakdown`: because ...
- `writing-plans`: because ...

**Use during implementation/review later:**
- `subagent-driven-development`: because ...
- `typescript-code-reviewer`: because ...

**Missing referenced skills:**
- `spike`: not present in `skills/spike/SKILL.md`; use `spec-driven-development` + `source-driven-development` + `planning-and-task-breakdown` unless/until created.

**Not using:**
- `...`: because ...
```

### Step 2：程式碼 reconnaissance

主 agent 先讀使用者指定檔案，再搜尋附近用法。大型或跨多目錄時派 read-only subagent。

必查項目：
- 指定檔案內容。
- 同資料夾相似 component / hook / utility。
- Route、父層 layout、data fetching / state flow。
- TypeScript types / API response shape。
- Shared UI component / wrapper。
- Tests、Storybook、mock data、i18n keys。
- Tailwind / AntD / AG Grid / form patterns。

Code reconnaissance subagent prompt 模板：

```text
你是 read-only code reconnaissance subagent。不要修改檔案。

Task goal:
[使用者目標]

Known files:
- [path]

Relevant local skills to check:
- React patterns: `react-dev`, `react-useeffect`, `react-state-management`
- TypeScript: `typescript-advanced-types`, `typescript-code-reviewer`
- Routing: `react-router-declarative-mode`, `react-router-data-mode`, `react-router-framework-mode`
- UI libraries: `ant-design`, `antd`, `ag-grid`
- Forms/i18n: `react-hook-form-zod`, `internationalization-i18n`
- Styling/design system: `tailwind-design-system`, `design-system-patterns`, `responsive-design`, `accessibility-compliance`

Investigate:
1. Read the known files and summarize what they do.
2. Find nearby usages / similar components / related tests.
3. Identify existing patterns for routing, state, data fetching, styling, i18n, forms, table behavior.
4. Identify which relevant local skills apply based on imports, file names, and patterns found.
5. Identify likely files to modify and files that should not be touched.
6. Identify risks, missing details, and questions for the user.

Return in Traditional Chinese with exact file references, applicable skill names, and concise bullets.
```

輸出：

```markdown
## Code Reconnaissance

**Files read:**
- `...`: why relevant

**Nearby patterns:**
- `...`: pattern

**Likely touch points:**
- Modify: `...`
- Test: `...`

**Do-not-touch / risky areas:**
- ...

**Questions from code:**
- ...
```

### Step 3：Figma / design reconnaissance

如果使用者有 Figma、截圖或設計描述，整理設計意圖，而不是只複製像素。

必查 / 必問面向：
- Layout：section、container、spacing、grid、auto layout。
- Component：是否對應 AntD / AG Grid / 專案 wrapper。
- Tokens：color、spacing、radius、typography、shadow、density。
- States：hover、focus、active、disabled、loading、error、empty、success。
- Responsive：desktop/tablet/mobile、breakpoints、overflow、collapse。
- A11y：focus order、keyboard、ARIA label、contrast、touch target。
- i18n：文案、長字串、日期/數字格式、pluralization。
- Data：真實資料長度、空值、權限、API error、large data。

Design reconnaissance subagent prompt 模板：

```text
你是 frontend design reconnaissance subagent。不要修改檔案。

Goal:
[使用者目標]

Design input:
[Figma / screenshot / description]

Existing code context:
[必要檔案摘要]

Relevant local skills to check:
- UI/design quality: `frontend-design`, `frontend-ui-engineering`, `web-design-guidelines`
- Design system/tokens: `design-system-patterns`, `design-system-starter`, `tailwind-design-system`
- Component libraries: `ant-design`, `antd`, `ag-grid`
- Responsive/a11y: `responsive-design`, `accessibility-compliance`
- Forms/i18n if visible in the design: `react-hook-form-zod`, `internationalization-i18n`

Analyze:
1. Extract UI requirements from the design.
2. Separate visual intent from implementation assumptions.
3. Map design elements to existing components/tokens where possible.
4. Identify which relevant local skills should guide the design-to-code mapping.
5. List missing states: loading, empty, error, disabled, hover, focus, validation, responsive.
6. Identify likely Figma-vs-code gaps and questions.

Return in Traditional Chinese with a requirement table, applicable skill names, and open questions.
```

輸出：

```markdown
## Design Reconnaissance

| Requirement | Figma / design evidence | Existing code mapping | Assumption | Open question |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

### Step 4：Gap analysis

把 Figma、現有 code、design system、產品需求的衝突分類，不直接做結論。

Gap 分類：
- Design stale：Figma 可能過時。
- Code debt：現有 code 可能需要改善。
- Design system gap：token/component 不支援。
- Product ambiguity：需求或資料流未定義。
- Intentional difference：現有產品是刻意不同。
- Implementation constraint：技術或 library 限制導致無法完全照設計。

輸出：

```markdown
## Gap Matrix

| Gap | Figma evidence | Code evidence | Category | Recommendation | Needs user decision? |
|---|---|---|---|---|---|
| ... | ... | ... | Product ambiguity | Ask user before planning | Yes |
```

### Step 5：列出 unknowns 並跟使用者討論

問題規則：
- 只問會影響 plan 的問題。
- 可查的先查，不要把查資料責任丟給使用者。
- 優先問 blocking questions。
- 一次問少量、有分組的問題。
- 若非 blocking，用 assumption 記錄並在 plan 中標明。
- 對使用者提出的 Clarifying Questions 必須使用中文（預設繁體中文）；程式識別字、路徑、命令、enum value、API 欄位與引用原文可保留英文，避免翻譯造成歧義。

常見問題類型：
- Figma 是否最新？哪些差異必須修？
- 要保留現有互動還是改成設計稿互動？
- 是否使用既有 AntD / AG Grid / shared component？
- 是否允許新增 token 或只能映射既有 token？
- 表格是否需要 sorting/filtering/pagination/selection？
- 表單 validation 何時觸發？錯誤訊息來源？
- 支援哪些 breakpoint？手機行為？
- 所有文案是否要 i18n？
- 驗收方式是 tests、storybook、screenshot、manual QA 還是全部？

輸出：

```markdown
## Clarifying Questions

> All user-facing questions in this section must be written in Chinese; keep code identifiers, paths, commands, enum values, API fields, and quoted source text unchanged when needed.

**Blocking before plan:**
1. ...

**Can proceed with assumptions:**
1. Assumption: ...; please confirm later.
```

### Step 6：網路 / 官方文件 research

先有 code/Figma 上下文，再做外部 research，避免泛泛搜尋。

網路查詢強制規則：
- 只要需要網路搜尋、官方文件查詢、issue / changelog 查證，或一般 web search / extraction 被阻擋，必須載入並使用 `playwright-mcp-usage`。
- `playwright-mcp-usage` 是本專案的 web lookup 入口；透過 Playwright MCP 真實瀏覽器 session 查詢，不把一般搜尋工具當成唯一來源。
- 查文字、表格、連結、欄位值時，優先用 DOM / accessibility snapshot；只有 DOM 不足、內容在 canvas/image、或需要驗證視覺狀態時才用 screenshot。
- UI 外觀、版面、modal、dropdown、可見性、spacing、顏色、overflow 等問題，優先用 screenshot，再用 DOM 補 exact text / attributes。
- 同一時間只控制一個 Playwright MCP browser/session；不同網站或任務要 sequentially 處理，避免 context 混淆。

搜尋優先順序：
1. 官方文件：React、TypeScript、Tailwind、AntD、AG Grid、react-hook-form、react-i18next、React Router。
2. W3C / MDN / WAI-ARIA：a11y 與 browser behavior。
3. 官方 issue / migration guide / changelog：版本差異。
4. 高品質工程文章：只有官方文件不足時使用。

Web research subagent prompt 模板：

```text
你是 web research subagent。不要修改檔案。

Question:
[需要查證的問題]

Project stack:
React, TypeScript, Tailwind, AG Grid React, Ant Design, react-i18next, react-router-dom, react-hook-form.

Relevant local skills to cross-check before web research:
- Required web lookup workflow: `playwright-mcp-usage`
- React / TypeScript: `react-dev`, `typescript-advanced-types`
- Tailwind / design system: `tailwind-design-system`, `design-system-patterns`
- Ant Design: `ant-design`, `antd`
- AG Grid: `ag-grid`
- Forms/i18n/router: `react-hook-form-zod`, `internationalization-i18n`, `react-router-declarative-mode`, `react-router-data-mode`, `react-router-framework-mode`
- Testing/a11y: `vitest-testing`, `playwright-best-practices`, `webapp-testing`, `accessibility-compliance`

Research rules:
1. Load and apply `playwright-mcp-usage` before doing any external web lookup.
2. Use Playwright MCP / browser-based access when normal web search or extraction is blocked; prefer DOM / accessibility snapshot for text/data extraction and screenshots for UI state.
3. Prefer official docs.
4. Include URLs.
5. State version caveats if visible.
6. Convert findings into concrete planning implications.
7. State which local skills the finding should feed into.
8. Do not suggest implementation beyond the asked scope.

Return concise Traditional Chinese summary with source table, access method, and applicable skill names.
```

輸出：

```markdown
## External Research

| Question | Source | Access method / skill used | Finding | Planning implication |
|---|---|---|---|---|
| ... | https://... | Playwright MCP via `playwright-mcp-usage` | ... | ... |
```

### Step 7：提出 approaches

在寫 plan 前，先提出 2-3 個方案讓使用者選擇。每個方案包含：
- 修改範圍。
- 是否符合現有 code pattern。
- 是否貼近 Figma。
- 風險與 tradeoff。
- 驗證成本。
- 推薦結論。

輸出：

```markdown
## Approach Options

### Option A: Minimal alignment with existing code
- Scope:
- Pros:
- Cons:
- Risks:
- Verification:

### Option B: Figma-first redesign with design-system mapping
- Scope:
- Pros:
- Cons:
- Risks:
- Verification:

**Recommendation:** Option ..., because ...
```

Gate：使用者未選方案前，不進入 final implementation plan；若只有一個合理方案，也要清楚列 assumptions 並請使用者確認。

### Step 8：撰寫 implementation plan

Plan 應該是實作交接包，不只是方向摘要。

必備結構：

```markdown
# [Feature / Task] Implementation Plan

> Use this plan only after the user approves the planning-phase decisions.
> Recommended implementation mode: subagent-driven-development.

## Goal

## Scope

### In scope

### Out of scope

## Decisions

| Decision | Source | Rationale |
|---|---|---|

## Relevant Findings

### Code findings

### Design / Figma findings

### External docs findings

## Architecture / Approach

## Naming Plan
- Generated code variable and function names must be descriptive and domain-specific; avoid abbreviations and over-generic names.
- Preserve important domain qualifiers from existing code or business concepts. Example: keep `SpcTable` in `isSpcTableEmptyVal` instead of shortening it to `isEmptyVal`.
- If implementation requires renaming existing symbols, list `old name -> new name` and the rationale.

## File Map

### Modify
- `...`: ...

### Create
- `...`: ...

### Tests / QA
- `...`: ...

### Avoid touching
- `...`: ...

## Task Breakdown

### Task 1: ...

**Objective:** ...

**Files:**
- Modify: `...`
- Test: `...`

**Steps:**
1. ...
2. ...

**Verification:**
- Run: `...`
- Expected: `...`

## UI / Figma Mapping

| Design element | Code component/token | Decision |
|---|---|---|

## States

- Loading:
- Empty:
- Error:
- Disabled:
- Hover/focus:
- Validation:

## Responsive Plan

| Breakpoint | Behavior |
|---|---|

## Accessibility Plan

## i18n Plan

## Test / QA Plan

## Risks

## Remaining Assumptions
```

### Step 9：Plan self-review

交給使用者前先做自檢。

Checklist：

```markdown
## Plan Self-review Checklist

- [ ] 每個使用者需求都有 task 對應。
- [ ] 每個 Figma/code gap 都有 decision、assumption 或 open question。
- [ ] 沒有 TBD、TODO、placeholder、模糊的「處理 edge cases」。
- [ ] File paths 來自實際 code reconnaissance。
- [ ] Task 順序能安全執行。
- [ ] 每個 task 有驗證方式與 expected result。
- [ ] UI states 覆蓋 loading / empty / error / disabled / hover / focus。
- [ ] Responsive 行為明確。
- [ ] A11y 檢查已納入。
- [ ] i18n / 長字串影響已納入。
- [ ] TypeScript types / runtime data assumptions 已列明。
- [ ] 生成 code 的 variable / function 名稱保持描述性與 domain-specific，沒有用簡寫或過度泛化名稱，也沒有移除重要 domain qualifier（例如不要把 `isSpcTableEmptyVal` 縮成 `isEmptyVal`）。
- [ ] Risks 與 rollback / stop conditions 已列明。
- [ ] 已列出 implementation phase 建議使用的 skills。
```

### Step 10：Plan review subagent

如果任務有多檔案、多 UI states、Figma 落差、或方案風險，派 plan-review subagent。

Plan review subagent prompt 模板：

```text
你是 planning-phase reviewer。不要修改檔案。

Original user goal:
[goal]

Code/design findings:
[summary]

Draft plan:
[plan]

Relevant local skills to check against the plan:
- Problem framing/spec: `brainstorming`, `spec-driven-development`, `planning-and-task-breakdown`
- Frontend implementation: `react-dev`, `frontend-ui-engineering`, `frontend-design`
- Stack-specific: `ant-design`, `antd`, `ag-grid`, `react-hook-form-zod`, `internationalization-i18n`, `react-router-declarative-mode`, `react-router-data-mode`, `react-router-framework-mode`
- Quality gates: `typescript-code-reviewer`, `accessibility-compliance`, `responsive-design`, `vitest-testing`, `playwright-best-practices`, `webapp-testing`, `qa-test-planner`, `verification-before-completion`
- External research / blocked web lookup: `playwright-mcp-usage`

Review for:
1. Missing requirements or misunderstood goal.
2. Figma-vs-code gaps that were not resolved.
3. Missing files, tests, states, responsive, a11y, i18n.
4. If external research is used or required, missing `playwright-mcp-usage` usage and missing access-method evidence.
5. Missing local skill usage for relevant stack areas.
6. Vague tasks or placeholders.
7. Risky assumptions that need user confirmation.
8. Over-engineering or scope creep.

Output:
- Verdict: PASS or REQUEST_CHANGES
- Critical gaps:
- Missing / misused skills:
- Important improvements:
- Minor suggestions:
```

Gate：若 reviewer 是 `REQUEST_CHANGES`，先修 plan，再交給使用者。

### Step 11：交付使用者並等待批准

交付格式：

```markdown
## Planning Result

**Recommended approach:** ...

**Important decisions needed:**
1. ...

**Plan file / plan content:**
...

**Ready for implementation only after you approve.**
```

此時不要自動開始實作，除非使用者明確說「開始做」、「照 plan 執行」、「go」。

---

## 5. Sub-agent 分工建議

| Sub-agent | 何時使用 | Tool scope | 任務 | 回傳格式 |
|---|---|---|---|---|
| Code reconnaissance | 相關檔案多、需要查附近用法 | read/search only | 讀指定檔案、找相似用法、找 tests/types/routes | File refs、patterns、risks、questions |
| Design/Figma analysis | 有 Figma/截圖/樣式落差 | read/vision/browser if available | 萃取 layout、states、tokens、responsive、a11y | Requirement table、gap candidates |
| Web research | 需要查官方 API / library behavior，或一般 web search / extraction 被阻擋 | web/browser/MCP；必須套用 `playwright-mcp-usage` | 查官方 docs、版本 caveat、planning implications；用 Playwright MCP 透過 DOM / screenshot 查證 | Source table + access method |
| Skill selector | 任務橫跨多技術或後續要寫 skill | file/search | 建議本任務該載入/後續該用哪些 skills | Skill list with reasons |
| Plan reviewer | Plan 複雜、風險高、Figma-code gap 多 | file/read only | 找漏項、模糊 task、未解決決策 | PASS / REQUEST_CHANGES |

規則：
- 不要讓 sub-agent 直接修改檔案，除非已進入 implementation phase。
- 不要讓 sub-agent 自己猜完整上下文；主 agent 要提供 goal、known files、constraints、output format。
- 不要把多個會互相衝突的 implementation 任務平行丟給 sub-agent；前期 workflow 以調查與 review 為主。
- Sub-agent 回傳必須包含 evidence，不接受只有結論。

---

## 6. 前期 workflow 的紀錄 artifact

建議每次前期任務都留下這些內容，可放在對話、issue、或後續 plan 文件中：

```markdown
# [Task] Preflight Record

## 1. Intake

## 2. Brainstorming Notes

## 3. Skill Selection

## 4. Code Reconnaissance

## 5. Design / Figma Reconnaissance

## 6. Gap Matrix

## 7. External Research

## 8. Clarifying Questions

## 9. Decisions

## 10. Approach Options

## 11. Draft Plan

## 12. Naming Plan

## 13. Plan Review Notes

## 14. Final Handoff
```

最重要的是 `Gap Matrix`、`Decisions`、`Remaining Assumptions`，因為 Figma 與現有產品有落差時，這些內容能避免後續實作 agent 照錯真相來源。

---

## 7. Definition of Done

前期 workflow 完成條件：

- [ ] 已讀使用者指定的相關檔案。
- [ ] 已查看附近用法 / 相似 component / tests / routes / shared utilities。
- [ ] 已完成 brainstorming：使用者意圖、已知事實、假設、未知、2-3 個方案與推薦方向。
- [ ] 已整理 Figma 或設計輸入，並標記與現有 code 的落差。
- [ ] 已列出會影響 plan 的 unknowns。
- [ ] 已和使用者討論 blocking details 或明確列出 assumptions；如需提問，問題已用中文表達，且必要的 code identifiers / paths / commands 保持原文。
- [ ] 已判斷應使用哪些 skills，以及哪些留到 implementation phase。
- [ ] 已查必要的官方 / 網路文件，並記錄 URL、access method，以及 `playwright-mcp-usage` 如何用於 Playwright MCP / DOM / screenshot 查證。
- [ ] 已提出方案與 tradeoffs，並取得使用者方向確認。
- [ ] 已寫出 implementation plan，含 exact paths、task breakdown、verification，以及生成 code 的命名規則 / naming plan。
- [ ] 已完成 plan self-review。
- [ ] 複雜任務已用 plan-review subagent 檢查。
- [ ] 使用者已收到 final plan，並知道下一步需批准後才實作。

---

## 8. 之後轉成 Skill 的建議

未來可把本 workflow 濃縮成 `skills/<skill-name>/SKILL.md`。建議名稱：

- `frontend-task-preflight`
- `frontend-planning-preflight`
- `figma-code-planning`

Skill description 不要摘要完整流程，避免模型只看 description 不讀正文。建議：

```yaml
description: Use when preparing a frontend coding task before implementation, especially when the user provides goals, code references, and Figma/design context that may differ from the current product.
```

Skill 主體建議保留：
- Non-negotiables：不寫 code、不改檔、先 explore/plan/discuss。
- Workflow steps：intake → code/design reconnaissance → gap analysis → questions → research → plan → review。
- Sub-agent prompt templates。
- Plan artifact template。
- Definition of Done。

大型內容可拆成 references：
- `references/subagent-prompts.md`
- `references/figma-gap-analysis.md`
- `templates/preflight-record.md`
- `templates/implementation-plan.md`

---

## 9. 對使用者原始流程的對應

| 使用者流程 | 本 workflow 對應 |
|---|---|
| 1. 使用者提供目標、相關程式碼位置、Figma 樣式 | Step 0 Intake |
| 2. 查看相關程式碼與附近使用 | Step 2 Code reconnaissance |
| 3. 思考如何達成、問題、未提細節 | Step 4 Gap analysis + Step 5 Unknowns |
| 4. 跟使用者討論目標細節 | Step 5 Clarifying questions + Step 7 Approach options |
| 5. 思考應使用什麼技能 | Step 1 Skill selection |
| 6. 搜尋網路相關資訊 | Step 6 External research |
| 7. 撰寫計劃 | Step 8 Implementation plan |
| 8. 回看是否計劃完整 | Step 9 Self-review + Step 10 Plan review subagent |
