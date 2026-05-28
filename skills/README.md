# Project Skills Staging

這個目錄是本專案的 AI coding agent skills staging / catalog。

每個可移植 skill 都採用 flat layout：

```text
skills/<skill-name>/SKILL.md
```

## 如何移植

依目標 agent 複製需要的 skill 子目錄：

```bash
# Claude Code
cp -a skills/<skill-name> .claude/skills/

# OpenCode
cp -a skills/<skill-name> .opencode/skills/

# Codex / Open Agent standard
cp -a skills/<skill-name> .agents/skills/

# Kilo Code
cp -a skills/<skill-name> .kilo/skills/
```

不要假設專案根目錄的 `skills/` 會被所有 agent 自動載入；它主要是 canonical staging 目錄。

## 索引與驗證

- `SKILLS_MANIFEST.md`：已下載 skills 的來源、commit、原始路徑與用途。
- `VALIDATION_REPORT.md`：frontmatter、secret/token pattern 與危險命令掃描結果。
