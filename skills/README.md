# VS Code Chat Personal Skills

這個目錄是要安裝至 `~/.copilot/skills/` 的 Agent Skills catalog。

每個可移植 skill 都採用 flat layout：

```text
skills/<skill-name>/SKILL.md
```

## 如何安裝

在 Repository 根目錄執行：

```bash
bash scripts/install-vscode-chat.sh
```

也可只複製需要的子目錄到 `~/.copilot/skills/`。不要假設 Repository 根目錄的 `skills/` 會被 VS Code 自動載入；它是 canonical source layout。

工作流相關 Skill 與 [custom agents](../agents/) 搭配，目標為 **VS Code Local＋BYOK**：Skill 保存程序和資源，Custom Agent 保存工具限制、handoff、worker allowlist 與 `agent/runSubagent` 編排。原生 Copilot 的 `task` 與設定格式需另外適配；見[相容性核對](./frontend-staged-review-workflow/references/vscode-copilot-compatibility.md)。

## 索引與驗證

- `SKILLS_MANIFEST.md`：已下載 skills 的來源、commit、原始路徑與用途。
- `VALIDATION_REPORT.md`：目錄、格式、參考連結、回歸測試及版本驗證的實際結果與限制。

## 2026-11-02 目錄狀態

目前共 60 個 Skills（30 core／30 on demand）。新增正式工作流 [azure-devops-create-pr](./azure-devops-create-pr/SKILL.md)，透過 Azure DevOps MCP 建立 PR，詢問 SPEC 與 work item ID，不驗證 work item，repository 範本無法取得時自動使用內建範本。

TDD、RHF、i18n 與設計指南已採其他主要來源並保留原名稱。專用無障礙與動畫效能套件不納入目錄；來源、移植限制與驗證請看 [更新報告](../docs/SKILL_REPLACEMENT_RESEARCH.zh-TW.md)。
