# Ubuntu VM：VS Code Chat Catalog 快速移植

本指南的目標是把整套 frontend catalog 一次放進 Ubuntu VM，讓 VS Code Chat 在所有專案中共用。

安裝完成後，Custom Agent 的中文使用方式與建議輸入格式請參考 [`AGENT_USAGE_GUIDE.zh-TW.md`](./AGENT_USAGE_GUIDE.zh-TW.md)。

## 最終位置

只複製這三類 runtime 資產：

```text
~/.copilot/
├── skills/
│   └── <skill-name>/SKILL.md
├── agents/
│   └── *.agent.md
└── instructions/
    └── *.instructions.md
```

不要把以下 VS Code Profile 檔案搬進 `~/.copilot`：

```text
~/.config/Code/User/chatLanguageModels.json
~/.config/Code/User/settings.json
~/.config/Code/User/prompts/*.prompt.md
```

BYOK API key、token 和其他 credentials 不包含在 bundle 中，也不應加入 Repository 或壓縮檔。

## 方法 A：VM 能連 GitHub（最簡單）

在 Ubuntu VM Terminal 貼上：

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-pip
git clone https://github.com/stu95256/frontend-skill.git
cd frontend-skill
bash scripts/install-vscode-chat.sh --dry-run
bash scripts/install-vscode-chat.sh
```

若已經 clone 過：

```bash
cd frontend-skill
git pull --ff-only
bash scripts/install-vscode-chat.sh
```

安裝器會合併檔案，不會刪除 `~/.copilot` 中其他名稱的個人自訂內容。

## 方法 B：複製單一壓縮檔到 VM

### 1. 在來源電腦建立 bundle

從 Repository root 執行：

```bash
bash scripts/build-vscode-chat-bundle.sh
```

產物：

```text
dist/frontend-skill-vscode-chat-bundle.tar.gz
```

### 2. 傳到 VM

可使用 VM shared folder、拖放、USB，或從來源電腦執行：

```bash
scp dist/frontend-skill-vscode-chat-bundle.tar.gz <vm-user>@<vm-ip>:~/
```

### 3. 在 Ubuntu VM 安裝

```bash
cd ~
tar -xzf frontend-skill-vscode-chat-bundle.tar.gz
cd frontend-skill-vscode-chat
bash scripts/install-vscode-chat.sh --dry-run
bash scripts/install-vscode-chat.sh
```

這四行是離線／共享資料夾移植時唯一需要在 VM 執行的安裝流程。

## 方法 C：直接複製三個資料夾

如果不使用安裝器，將 Repository 中的 `skills`、`agents`、`instructions` 複製到 VM 後執行：

```bash
mkdir -p ~/.copilot/skills ~/.copilot/agents ~/.copilot/instructions
cp -a /path/to/copied-catalog/skills/. ~/.copilot/skills/
cp -a /path/to/copied-catalog/agents/. ~/.copilot/agents/
cp -a /path/to/copied-catalog/instructions/. ~/.copilot/instructions/
```

不要只複製 `SKILL.md`；每個 Skill 旁邊的 `references/`、`scripts/`、`templates/`、assets 與 license 都必須保留。

## BYOK 與 VS Code Profile

如果 VM 是全新 VS Code Profile，BYOK 設定要在 VM 的 VS Code 中另外建立。設定位置是：

```text
~/.config/Code/User/chatLanguageModels.json
~/.config/Code/User/settings.json
```

若從另一台 Ubuntu 搬 Profile，關閉 VS Code 後可複製上述檔案，但必須自行安全地重新設定 credentials。不要從 Repository bundle 還原 secrets。

在 `settings.json` 確認：

```json
{
  "chat.agentHost.byokModels.enabled": true,
  "chat.subagents.allowInvocationsFromSubagents": false
}
```

BYOK 模型必須支援 tool calling。Coordinator 需要 `agent/runSubagent` 才能執行 hidden workers。

## 安裝後檢查

1. 完全關閉並重新開啟 VS Code，或執行 **Developer: Reload Window**。
2. 執行 **Chat: Open Customizations**。
3. 確認看到 Skills、Agents、Instructions。
4. 在 Chat 的 Tools 選單確認 `agent/runSubagent` 已啟用。
5. 開啟 Chat **Diagnostics**，確認沒有 invalid frontmatter、missing resource 或 duplicate name。
6. 選擇 **Frontend Task Preflight** 做一次測試。

檔案數量快速檢查：

```bash
find ~/.copilot/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l
find ~/.copilot/agents -maxdepth 1 -name '*.agent.md' | wc -l
find ~/.copilot/instructions -maxdepth 1 -name '*.instructions.md' | wc -l
```

本 bundle 應至少安裝：

```text
67 skills
14 custom agents
2 instruction files
```

「至少」是因為 `~/.copilot` 可能已包含其他個人 customization。

## 可選：在 VM 驗證 bundle 本身

在解壓後的 `frontend-skill-vscode-chat` 目錄執行：

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill_catalog.py
python3 -m unittest -v tests/test_vscode_conversion.py
```

預期 catalog validator 顯示：

```text
VS Code Chat catalog validation passed: 67 skills, 14 custom agents, 2 instruction files, no legacy runtime artifacts
```

## 更新與移除

更新時重新執行安裝器即可覆蓋同名 catalog 檔案：

```bash
bash scripts/install-vscode-chat.sh
```

這是 merge install，不會自動刪除已從新版 catalog 移除的舊檔。若曾安裝舊 Kilo／早期版本，先備份 `~/.copilot`，再手動刪除確認已淘汰的 customization；不要直接清空整個 `~/.copilot`，以免刪除其他個人資產。
