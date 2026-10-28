# Skills 跨來源更新與範圍調整

更新日期：2026-10-28（Asia/Taipei）。

## 本輪結果

依使用者最新指定，停止評估無障礙實作及動畫效能專項，移除既有兩個無障礙專用套件、專用參考文件與工作流選擇規則。先前已排除的頁面自動化測試套件維持排除。

目前為 **61 個 Skills（30 core／31 on demand）、14 個 Custom Agents、2 份 instructions**。沒有新增 Skill 名稱；四個既有 Skill 已改採其他主要來源，原名稱保留，既有代理可繼續選用。

一般元件的原生控制項、標籤、錯誤訊息與狀態處理仍是前端範例的一部分；它們不會觸發專用無障礙稽核或額外派工。

## 已完成的跨來源更新

| 現有 Skill | 新主要來源 | 實際變更 | 保留內容與適配 |
|---|---|---|---|
| [test-driven-development](../skills/test-driven-development/SKILL.md) | [Matt Pocock：tdd](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/tdd) | 主要入口與測試品質文件改採公開介面、獨立預期值、逐項行為驗證與適當 mock 邊界 | 保留 red-green-refactor；使用已授權的測試邊界，不反覆要求確認，不因程式碼早於測試便刪除重做；Git scope 仍由審查工作流決定 |
| [react-hook-form-zod](../skills/react-hook-form-zod/SKILL.md) | [Supabase：react-hook-form](https://github.com/supabase/supabase/blob/167c633ed06da4da7b545f083b999fd7d8c669c5/.agents/skills/react-hook-form/SKILL.md) | 重寫入口，加入訂閱、背景刷新、dirty/reset、數值空值與 server-backed 表單範例 | 保留 SecondSky 的 Zod、field array、多步驟與相關模板；去除 Studio 元件、lint 政策與外部 Skill 依賴；按安裝版本驗證 API |
| [internationalization-i18n](../skills/internationalization-i18n/SKILL.md) | [i18next 官方：i18next-localization](https://github.com/i18next/i18next-cli/tree/740a925c2a2b93e37c427bfd1a798708e68b7431/skills/i18next-localization) | 加入版本相符 CLI、dry-run、字串擷取與檢查、ICU／MF2 條件分流 | 保留原有 Intl、RTL、namespace、SSR 及其他框架資料；預設儲存庫語系檔，不自動採用服務、不提交或覆寫代理設定 |
| [frontend-design](../skills/frontend-design/SKILL.md) | [Impeccable](https://github.com/pbakaus/impeccable/tree/8409a564d1baee90b2dde4f7a8f06288838e3921/.github/skills/impeccable) | 改採 Persuade／Operate／Read／Experience 情境分類及設計品質文件 | 保留 Anthropic 的視覺方向原則；只移植文件，不攜帶 launcher、hooks、額外代理、即時頁面工具或被排除的專項流程 |

這是實際來源切換，不只是同一上游的版本更新。RHF 與 i18n 保留舊來源的適用文件，並在 metadata、manifest 與授權檔中分別記錄。

### 表單驗證帶來的修正

新增的 [server-backed 表單](../skills/react-hook-form-zod/templates/server-backed-form.tsx) 以字串作為欄位輸入，經 Zod 驗證後輸出數值；儲存後使用伺服器回應重設基準。

實際測試發現：若在 useForm.resetOptions 設定保留 dirty values，儲存完成或 Cancel 的 reset 也可能延續該策略，導致編輯值沒有被重設。範例已在這兩類 reset 明確關閉保留選項，並寫入 [生命週期指引](../skills/react-hook-form-zod/references/form-lifecycle.md)。背景刷新仍保留使用者編輯。

## 其餘候選的處理

| 候選類型 | 本輪處理 | 理由 |
|---|---|---|
| 無障礙實作、色彩對比與相關專用候選 | 不採用，停止後續調查 | 使用者已排除這類專項 |
| 動畫效能候選 | 不採用 | 使用者已明確排除；沒有加入任何這類 Skill |
| 通用 UI baseline／精修套件 | 不整包新增 | 設計主指南已更新；額外入口容易重疊或強制更換技術棧 |
| Orval | 保留為工具選擇參考 | 產生 client/hooks/schema 與現有純型別工作不同；不為更新 Skill 而遷移工具 |
| Lingui／TanStack Table | 按技術棧保留候選地位 | 不把 react-i18next、RHF 或 AG Grid 換成不同函式庫；Table v9 指引不可套用至 v8 |
| axross 專項套件 | 不複製進目錄 | 查核的固定快照未見明確授權檔 |
| Trail of Bits 深度差異審查 | 未併入預設工作流 | 原流程的 Git 範圍、輸出與派工契約不同，並非一般前端審查的直接替代 |

React Router、shadcn、AG Grid、Ant Design、Vercel React、Vitest、React Doctor 與本地審查／除錯流程保留前一輪已更新版本。沒有找到範圍相當且足以取代它們的其他來源，因此不為增加更新數量而替換。

## 來源與授權

下表為本輪四個新主要來源的固定快照。日期是 repository HEAD 的 committer UTC 日期，不是每個 Skill 的最後修改日。

| 來源 | 固定 SHA | HEAD 日期 UTC | 授權／範圍 |
|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c) | `59db609eb1e18aaf59b63284d0e52255aff0c63c` | 2026-10-27 | MIT；TDD 入口與測試參考 |
| [supabase/supabase](https://github.com/supabase/supabase/tree/167c633ed06da4da7b545f083b999fd7d8c669c5) | `167c633ed06da4da7b545f083b999fd7d8c669c5` | 2026-10-28 | Apache-2.0；RHF 入口與生命週期 |
| [i18next/i18next-cli](https://github.com/i18next/i18next-cli/tree/740a925c2a2b93e37c427bfd1a798708e68b7431) | `740a925c2a2b93e37c427bfd1a798708e68b7431` | 2026-10-27 | MIT；CLI 工作流 |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/8409a564d1baee90b2dde4f7a8f06288838e3921) | `8409a564d1baee90b2dde4f7a8f06288838e3921` | 2026-10-28 | Apache-2.0；選定設計文件 |

SecondSky 保留文件的 SHA 為 `88378361314f558fb719aec0af9fd898ab36f0b2`；Anthropic 保留設計來源的 SHA 為 `dbd4588f9e1033efb41dad4bef2f7947c8993d44`。原授權保留，新來源的授權分別放入對應 Skill，沒有把混合來源統一標成 MIT。

完整來源與每項版本請見 [來源政策](../SKILL_SOURCES.md) 與 [Skill manifest](../skills/SKILLS_MANIFEST.md)。

## 安裝與封裝

安裝器維持合併個人目錄，會清除本次退役及明確排除的已安裝專項，不刪除其他個人自訂資料。目錄驗證與回歸測試也會拒絕重新引用退役的 Skill。

發行封裝使用目前 canonical source 重建；數量、解壓驗證、7z 完整性與 Base64／SHA-256 回轉結果記錄於 [驗證報告](../skills/VALIDATION_REPORT.md)。

## 驗證界線

本輪已做來源查核、格式／連結檢查與實際範例驗證。完整命令與結果見 [驗證報告](../skills/VALIDATION_REPORT.md)。

機械驗證和單一工具範例不等於模型效果評測；尚未做同題模型 A/B、token／速度比較，也未驗證目標 Ubuntu profile 的 VS Code 發現與 BYOK 派工。設計文件沒有被宣稱已通過即時畫面檢查。
