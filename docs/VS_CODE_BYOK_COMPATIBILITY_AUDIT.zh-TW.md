# VS Code Local／Copilot BYOK 相容性核對

核對日期：2026-11-02。目標為 **VS Code Local＋支援 tool calling 的 BYOK 模型**。原生 Copilot harness 使用不同的 `task` 與 agent schema，本次沒有建立原生 Copilot 版本；`target: vscode` 不會切換 session harness。[官方 agent file 規格](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)

## 範圍與結論

盤點 60 個 Skill entrypoints、10 個 custom agents、2 份 instructions，並搜尋 supporting references、templates、scripts、安裝／打包／測試程式及使用文件中的 host API、委派、模型與發現位置假設。人工核對集中在會影響實際執行的指令；框架教學範例並未逐一建立應用執行。

本次已修正下列不一致；靜態／腳本驗證通過，實際目標 Profile 的模型派工仍需 session 驗證。

| 問題 | 修正與來源 |
|---|---|
| 只有 review coordinator 有頂層 guard | [Implementation](../agents/frontend-implementation.agent.md) 與 [Skill Creator](../agents/vscode-skill-creator.agent.md) 也加 invocation guard／`needs_parent_dispatch`；三個流程都保持 inline、單層委派。7 個 workers 均明列 `agents: []`。 |
| named worker 缺失時改派匿名角色 | [SDD](../skills/subagent-driven-development/SKILL.md) 與 [Skill Creator](../skills/skill-creator/SKILL.md) 明定完整 `agentName`／`description`／`prompt`；缺所需角色記錄 blocked。Local 匿名呼叫繼承 parent 的指令／工具，無法當成等價的角色替代。[官方 subagents](https://code.visualstudio.com/docs/agents/run/subagents) |
| AG Update 子文件要求 worker 問使用者／寫檔 | [scope](../skills/ag-update/references/determine-scope.md) 由 worker 回候選清單，parent 詢問；[changes](../skills/ag-update/references/determine-changes.md) 回完整建議內容／缺口，parent 驗證並寫入。沒有相容角色時在 parent 執行。 |
| 合法 VS Code frontmatter 被 quick validator 拒絕 | [validator](../skills/skill-creator/scripts/quick_validate.py) 接受四個 Local 可選欄位並驗證型別／值，明確讀 UTF-8；[packager](../skills/skill-creator/scripts/package_skill.py) 修正直接執行時的 import。`.skill` 匯出仍是 ZIP，不會自動安裝到 VS Code。 |
| 評估 prompts 被當成已註冊 worker，並假設有完整 transcript | [Skill Creator](../skills/skill-creator/SKILL.md) 與 retained grader／comparator／analyzer 說明相容角色前提；read-only worker 回 JSON 由 parent 儲存；只使用實際收到的 final results／artifacts。缺獨立評估或 transcript 就記錄限制。 |
| 把完整 Skill 當作 Local 呼叫的 system-prompt 參數 | [writing-skills](../skills/writing-skills/SKILL.md) 改用完整 `prompt`，保留 named role 的實際優先順序並檢查 baseline 汙染。 |
| 假設 agent 能刪除／重排既有 chat history | [context-engineering](../skills/context-engineering/SKILL.md) 區分新 packet、durable summary 與 host compaction；75% 是有 usage 資訊時的建議值，不是 VS Code 設定。[官方 context 說明](https://code.visualstudio.com/docs/agents/concepts/context) |
| Local 安裝範例要求開啟 Agent Host BYOK | [setup](./VS_CODE_CHAT_SETUP.zh-TW.md) 與 [VM guide](./VM_COPY_GUIDE.zh-TW.md) 區分 Local 與原生 Copilot；該開關只處理 Agent Host 的實驗性 BYOK。另說明 provider token limits、utility models 和 Copilot-backed search 的差異。[官方 BYOK](https://code.visualstudio.com/docs/agent-customization/language-models) |

## 發現位置與安裝

安裝器仍將完整 catalog 複製到 `~/.copilot`，保留其他個人資產，不修改 Profile、credentials 或實際 session。`skills/` 是支援的 personal Skill 位置；Repository 根目錄的同名資料夾本身只是來源 layout。

Local UI 建立的個人 agents／instructions 可使用 Profile storage；目前[上游位置定義](https://github.com/microsoft/vscode/blob/main/src/vs/workbench/contrib/chat/common/promptSyntax/config/promptFileLocations.ts) 也列出 `~/.copilot/agents` 與 `~/.copilot/instructions`。因此不能把「UI 建立位置」誤當成「唯一搜尋位置」，也不能只憑複製成功就聲稱已載入。尤其使用安裝器自訂 target 時，應以 Open Customizations／Diagnostics 核對來源，需要時設定額外發現位置，避免重複角色。[官方 custom agent discovery](https://code.visualstudio.com/docs/agent-customization/custom-agents#local-harness-locations-and-migration)

`context: fork` 是實驗功能且另有啟用設定，本套件的協調流程不依賴它。Skill 的 metadata 也不能代替 agent 的有效工具／權限。[官方 Skill 格式](https://code.visualstudio.com/docs/agent-customization/agent-skills)

## 保留的跨平台／歷史資料

- Anthropic authoring reference、Claude 測試案例、visual companion 分平台啟動範例與 skill-scanner 風險矩陣保留，但補上適用範圍；外來工具名稱不會被當作 Local API。
- 根目錄早期 research files 與舊 validation 段落是有日期的歷史記錄，不能取代目前安裝指南。
- [Base64 傳輸說明](../base64-transfer/README.md) 改為明確標示既有快照。本次沒有重建舊 binary／Base64 分發檔；SHA-256 僅證明傳輸完整，不代表版本新鮮。需要最新包時從目前來源執行 [bundle builder](../scripts/build-vscode-chat-bundle.sh)。

## 本次驗證與限制

- Catalog validator：60 Skills、10 custom agents、2 instruction files 通過。
- 60 個 Skills 同時通過快取的官方 Agent Skills reference validator（`69ef37e` checkout）與 bundled Local quick validator；沒有更新或安裝套件。
- 9 個 regression tests 全數通過，沒有 skip，包括 isolated install／retired entry 清理、SDD helpers、holdout isolation，以及新增的 Local frontmatter／中文路徑／從其他 cwd 打包測試。Git Bash 安裝 fixture 在 sandbox 內無法建立 temp target，改在 sandbox 外跑測試後通過；未安裝到真正的個人 catalog。
- 安裝器與 bundle builder 的 Bash syntax 通過。獨立桌上推演確認缺 evaluator 時 blocked、coordinator 被誤派時回 `needs_parent_dispatch`；這不是實際 VS Code subagent E2E。
- 尚未驗證目標 Ubuntu／Windows Profile 的實際 named-worker 調用、特定 BYOK provider 的回應大小、Azure MCP 連線或模型效果；未把文件／JSON 輸出規約當成 host 強制保證。

完整呼叫與證據交付規則見[共用相容性文件](../skills/frontend-staged-review-workflow/references/vscode-copilot-compatibility.md)。
