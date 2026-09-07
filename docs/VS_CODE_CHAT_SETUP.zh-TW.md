# Ubuntu VS Code Chat / Copilot BYOK 安裝與驗證

## 安裝位置

將本 Repository 的三個 runtime 目錄合併到個人 Copilot 目錄：

```text
~/.copilot/
├── skills/
├── agents/
├── instructions/
└── hooks/          # 本專案刻意不提供全域 hook
```

執行：

```bash
bash scripts/install-vscode-chat.sh --dry-run
bash scripts/install-vscode-chat.sh
```

安裝器只會合併本專案提供的檔案，不會清除 `~/.copilot` 中其他自訂內容，也不會修改 VS Code 設定或 BYOK credentials。

## VS Code 設定

BYOK Provider 與模型設定仍屬於目前的 VS Code Profile；不要搬入 `~/.copilot`。Ubuntu 預設 Profile 使用：

```text
~/.config/Code/User/chatLanguageModels.json
~/.config/Code/User/settings.json
~/.config/Code/User/prompts/*.prompt.md
```

命名 Profile 則位於 `~/.config/Code/User/profiles/<profile-id>/`。在該 Profile 的 `settings.json` 檢查：

```json
{
  "chat.agentHost.byokModels.enabled": true,
  "chat.subagents.allowInvocationsFromSubagents": false
}
```

- 本 catalog 的 Skills 使用標準 inline 載入，不依賴實驗性的 `context: fork`。
- 本套件的 coordinator 直接建立 worker subagents，不需要 nested subagents，因此預設保持 `false`。
- BYOK 模型必須支援 tool calling，才能使用檔案、terminal、Skill 與 `agent/runSubagent`。

本 catalog 不建立 Prompt files：原本的多步 workflow 已依語意轉成 Agent Skill 與 custom agent，而不是依賴非官方的 `.workflow.md`。也不提供全域 Hook，避免在所有 Repository 無條件執行語言或 package-manager 特定命令。

## 驗證載入

1. 重新載入 VS Code 視窗。
2. 執行 **Chat: Open Customizations**，確認 Skills、Agents、Instructions 均出現。
3. 在 Chat 視窗開啟 **Diagnostics**，確認沒有 invalid name、frontmatter 或 missing resource 錯誤。
4. 在 Tools 選單啟用 `agent/runSubagent`。
5. 選取 **Frontend Task Preflight**，確認完成後出現 **Implement Approved Plan** handoff。
6. 選取 **Frontend Review** 並要求 staged review；在測試 Repository 暫存小型 diff，確認主 Agent 顯示兩個以上獨立 `Frontend Reviewer` subagent calls。
7. 執行 Repository validator：

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill_catalog.py
python3 -m unittest -v tests/test_vscode_conversion.py
```

## 工作流入口

| 需求 | Custom Agent |
|---|---|
| 實作前研究、方案與核准 | Frontend Task Preflight |
| 執行已核准計畫 | Frontend Implementation |
| Debug 並修正 | Frontend Debug |
| Review `git diff --cached` | Frontend Review（staged mode） |
| 高冗餘 staged review | Frontend Review（heavy staged mode） |
| Review branch merge-base 到 source 的貢獻 | Frontend Review（branch mode） |
| 根據 staged diff 產生單行 commit subject | `/frontend-staged-commit-message` Agent Skill |

各 user-facing Agent 的適用情境、附件建議、最小輸入與完整輸入模板，請參考 [`AGENT_USAGE_GUIDE.zh-TW.md`](./AGENT_USAGE_GUIDE.zh-TW.md)。

Worker agents 設定 `user-invocable: false`，這是 VS Code 官方文件中「不顯示在 picker、但仍可作為 subagent」的標準做法。Worker 不設定 `disable-model-invocation: true`，因為該欄位會禁止一般模型呼叫；各 coordinator 仍以明確的 `agents` allowlist 限制自己可選用的 worker。

## Subagent 方法核對

本 catalog 使用的是 VS Code Chat 原生 Coordinator/Worker 方法：

```yaml
tools: [agent, read, search]
agents:
  - Frontend Reviewer
```

Coordinator 的正文以 `#tool:agent/runSubagent` 明確要求工具呼叫。`agents` 中的名稱區分大小寫，必須與 worker 的 `name` 完全一致。每次呼叫都是 stateless one-shot；重試會建立新的 invocation，並重新提供完整任務、限制和預期輸出。

本 catalog 的 worker 沒有 `agent` tool，也沒有自己的 `agents` allowlist，因此不會建立 nested subagents。`chat.subagents.allowInvocationsFromSubagents` 維持 `false`。

`context: fork` 是另一種「整個 Skill 在隔離 subagent 執行」的 VS Code 功能，不是本 catalog 多 worker workflow 的編排機制。Coordinator workflows 不使用 `context: fork`，避免在 forked skill 裡形成預設禁止的第二層 subagent。

## 官方規格

- [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Subagents](https://code.visualstudio.com/docs/agents/run/subagents)
- [Custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [Language models / BYOK](https://code.visualstudio.com/docs/agent-customization/language-models)
