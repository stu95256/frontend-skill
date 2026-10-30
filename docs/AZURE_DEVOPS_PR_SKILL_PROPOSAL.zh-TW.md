# Azure DevOps PR Skill 研究與建議

研究日期：2026-10-30。

建議新增 `azure-devops-create-pr`：讀取已提交的分支差異，詢問要納入 description 的 SPEC 與要關聯的 work item ID，收到回答後透過 Azure DevOps MCP 自動建立 PR，不主動查詢或驗證 work item。

完整可檢閱草案位於 [SKILL.md](./proposals/azure-devops-create-pr/SKILL.md)。本次交付為設計提案，草案放在文件區，尚未加入正式 Skill catalog 或安裝流程，也沒有建立實際 PR。

## 網路上找到的參考

以下均閱讀原始作者 repository 的內容；新草案為依需求重新撰寫，沒有整份複製第三方 Skill。

| 參考 | 可採用的做法 | 本需求需要調整之處 |
| --- | --- | --- |
| [Microsoft Aspire：create-pr Skill](https://github.com/microsoft/aspire/blob/main/.agents/skills/create-pr/SKILL.md) | 讀取分支、套用 repository PR template、自動建立 PR，以及避免重複建立。 | 使用 GitHub CLI；本提案改以 Azure DevOps MCP 執行遠端操作，並加入 SPEC 與 work item 的必要詢問。 |
| [tomzx/agents：create-pr Skill](https://github.com/tomzx/agents/blob/main/skills/create-pr/SKILL.md) | 以實作差異撰寫結構化 description，呈現需求與變更之間的關係。 | 原流程會讀 issue 並包含 reviewer、視覺證據等周邊流程；本提案僅依使用者選定的 SPEC 組織內容，不查 work item、不自動增加 reviewer。 |
| [Microsoft HVE Core：Azure DevOps PR workflow 說明](https://github.com/microsoft/hve-core/blob/main/docs/agents/ado-backlog/pr-creation.md) | 讓專責 PR 流程處理 Azure DevOps repository 操作與 work item 關聯。該頁是流程文件，並非直接可安裝的 Skill。 | 原流程包含 work item discovery、reviewer 識別與更多確認。本需求改成直接接收 ID；資料齊全後自動建立。 |

這些來源分別提供 template、需求導向 description 與 Azure DevOps 串接方式；本次未找到可直接套用、同時符合「詢問 SPEC、詢問 work item、略過 work item 驗證」全部條件的現成 Skill，建議建立專用版本。

## MCP 選擇與工具相容性

這裡的「azure mcp」解讀為 **Azure DevOps MCP Server**。Microsoft 的 [MCP catalog](https://github.com/microsoft/mcp) 分別列出 Azure 資源管理與 Azure DevOps 的 MCP；建立 Azure Repos PR 應使用後者。

依 [官方 Azure DevOps MCP 說明](https://github.com/microsoft/azure-devops-mcp)，目前官方建議優先使用 remote server，local stdio server 也仍受支援。Skill 不需要替使用者更換既有連線。

依 [官方 Toolset](https://github.com/microsoft/azure-devops-mcp/blob/main/docs/TOOLSET.md)，目前工具正朝 action 式介面調整。下表為研究時的文件名稱，實際執行須以連線公布的 schema 為準，不能直接假定某個版本或任意填入參數：

| 目的 | 文件中的工具與 action |
| --- | --- |
| repository 與 default branch | `repo_repository` / `get` |
| 查詢重複 PR | `repo_pull_request` / `list` |
| 建立 PR | `repo_pull_request_write` / `create` |
| 建立後關聯 work item | `wit_work_item_link_write` / `link_to_pull_request` |

舊版本可能使用 `repo_create_pull_request` 等獨立工具名稱，草案要求先 discovery。建立工具若能直接接收 work item IDs，優先在建立時傳入；否則建立 PR 後再呼叫關聯工具。兩種方式都不需要 agent 預先讀取 work item。

「不檢查 work item」是指 agent 不做 existence、內容、狀態或關聯合理性查詢。Azure DevOps 在收到建立或關聯請求時仍可能拒絕 ID；Skill 會回報服務端結果，不將這項限制誤稱為可略過的服務端驗證。

## 建議的互動流程

```text
使用者：幫目前分支建立 Azure DevOps PR
    ↓
解析 repo／source／target、工具 schema、已提交的 diff、PR template
    ↓
已有相同 source → target 的 active PR？有則回傳連結
    ↓
一次詢問尚未提供的資料：
  1. description 要包含哪些 SPEC？可以多個，也可以回答「無」。
  2. 要關聯哪些 work item ID？可以多個，也可以回答「無」。
    ↓
等待使用者回答，依 diff + 選定 SPEC 產生 title／description
    ↓
必要時正常 push 已提交的 source branch
    ↓
透過 MCP 建立 PR，傳入 IDs 或在建立後直接關聯
    ↓
回傳 PR URL 與關聯結果
```

例如 Skill 會問：

> 這次 PR 的 description 要包含哪些 SPEC？可提供文件路徑、連結、SPEC 編號或直接貼內容；沒有請填「無」。
>
> 要關聯哪些 work item ID？例如 12345、12346；不關聯請填「無」。我會直接使用你提供的 ID，不查詢或驗證 work item。

已在本次任務中明確提供的資料不重問。沒有回答時保持等待，不能將沉默當成「無」。一般建立 PR 的指令已授權建立與上述關聯，回答齊全後直接執行；使用者明確要求先看 description 時，才先提供預覽並等待其確認。

## Description 設計

優先遵循 repository 現有的 Azure Repos template。依 [Azure Repos 官方 template 規則](https://learn.microsoft.com/en-us/azure/devops/repos/git/pull-request-templates)，template 取自 default branch，並區分 target branch 專用與預設 template；草案會依這些規則讀取。

Skill 資料夾內提供 [備用 PR 範本](./proposals/azure-devops-create-pr/assets/pr-description.md)，包含 `Summary`、`Changes`、`SPECs`、`Work Items`、`Validation`。找不到適用的 repository template、讀到空內容，或因權限、網路、逾時、缺少讀檔工具而無法取得時，自動使用這份備用範本，不額外詢問使用者，也不因範本讀取失敗而中止建立 PR。PR 建立本身所需的權限與工具仍須具備。

建立 description 前會替換所有範本變數，並依 PR 使用語言調整標題與內容。SPEC 可有多個，保留使用者提供的識別資訊，僅摘要已讀取且與 diff 相符的內容。只拿到連結或 SPEC ID 也可以建立；不捏造需求已完成或驗收通過。

Work item 同時列入 description，並透過 API 實際關聯。description 裡的 `#12345` 文字不等同工具已成功建立關聯；若連線沒有關聯能力，先說明限制，取得使用者接受後才能改採僅列文字的方式。

## 與既有 TypeScript reviewer 的關係

你指定的 [typescript-code-reviewer](../skills/typescript-code-reviewer/SKILL.md) 專注在 TypeScript／TSX 缺陷 review；建議保留其原本職責，新增獨立 PR Skill。

若使用者要求「先 review 再建立 PR」，可先執行現有 review 流程，再把對應 source commit 的實際結果放進 Validation。單純建立 PR 時不強制 review，不自動加上測試、修正程式或 reviewer 派送流程。

## 行為驗收情境

這些是草案設計的人工檢查情境，尚未透過真實 Azure DevOps MCP 做端到端測試。

| 情境 | 預期行為 |
| --- | --- |
| 尚未提供 SPEC 和 work item | 合併詢問並等待回答，尚不建立 PR。 |
| 已提供 SPEC，未提供 work item | 只詢問 work item。 |
| 成功取得適用的 repository template | 優先使用 repository template，補上缺少的 SPECs／Work Items 區塊。 |
| repository template 不存在、空白或無法讀取 | 自動讀取 Skill 內建範本，不額外確認；送出前替換全部變數。 |
| 提供多份 SPEC、多個 ID | 全部選定 SPEC 列入 description；使用者提供的 ID 交給建立／關聯工具。 |
| 兩項都明確回答「無」 | 不再追問；符合其他建立條件時自動建立。 |
| SPEC 是 work item 的連結 | 僅列引用，不為讀 SPEC 而查詢 work item。 |
| 使用者輸入不存在的 ID | 不預查；讓服務處理 create/link 請求，失敗時回報原錯誤與已建立的 PR。 |
| 部分 work item 關聯失敗 | 保留已建立 PR，分別回報成功與失敗；不重建。 |
| source／target 已有 active PR | 回傳既有 URL；沒有明確更新指令就不覆寫。 |
| PR 建立 timeout | 先查相同 source／target 是否已有 PR，不盲目再次建立。 |
| 有未提交檔案 | 僅描述已提交 diff，說明未提交檔案不在此次 PR 內；不自動 commit。 |
| 只有 Azure 資源 MCP，沒有 PR 建立能力 | 回傳完成的 title／description 與缺少的能力；不宣稱已建立。 |
| 提供的測試紀錄對應另一個 commit | 不宣稱目前 PR 驗證通過。 |

## 採用方式

建議名稱為 `azure-devops-create-pr`，搭配已連接且具有 PR 寫入權限的 Azure DevOps MCP。草案為單一 Skill，不需要客製 Azure SDK script 或另一個 coordinator agent。

正式採用時，再將 [Skill 草案](./proposals/azure-devops-create-pr/SKILL.md) 納入 catalog、來源 manifest 與數量檢查。這些安裝整合不屬於本次「研究並建議新 Skill」的交付範圍。
