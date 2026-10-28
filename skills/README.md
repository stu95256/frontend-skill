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

工作流相關 Skill 與 `../agents/*.agent.md` 搭配：Skill 保存程序和資源，Custom Agent 保存工具限制、handoff、worker allowlist 與 `agent/runSubagent` 編排。

## 索引與驗證

- `SKILLS_MANIFEST.md`：已下載 skills 的來源、commit、原始路徑與用途。
- `VALIDATION_REPORT.md`：目錄、格式、參考連結、回歸測試及版本驗證的實際結果與限制。

## 2026-10-28 更新

目前共 61 個 Skills（30 core／31 on demand）。TDD、RHF、i18n 與設計指南已採其他主要來源並保留原名稱。專用無障礙與動畫效能套件不納入目錄；來源、移植限制與驗證請看 [更新報告](../docs/SKILL_REPLACEMENT_RESEARCH.zh-TW.md)。
