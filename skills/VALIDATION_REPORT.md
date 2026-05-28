# Skills Validation Report

日期：2026-05-28

## 結果摘要

- 安裝位置：`skills/`
- skill 目錄數：59
- 檔案數：408
- `SKILL.md` frontmatter 檢查：通過
- `name` 與目錄名稱一致性：通過
- 高風險命令掃描：未發現 `rm -rf /`、`curl | sh`、`wget | sh`、`sudo rm -rf`、`dd if=` 類型命令
- secret / token 掃描：沒有發現真實 token；只有範例文字 false positives

## Secret 掃描 false positives

以下命中都是文件中的教學範例，不是真實憑證：

| 檔案 | 命中內容 | 判定 |
|---|---|---|
| `code-review-excellence/reference/security-review-guide.md` | `password: "super-secret-password"` | 反例示範：提醒不要把 secrets 放在 config |
| `playwright-best-practices/advanced/authentication-flows.md` | `const mockToken = 'test-verification-abc123';` | 測試 mock token 範例 |
| `playwright-best-practices/advanced/third-party.md` | `clientSecret: "pi_mock_123_secret_mock"` | Stripe mock payment intent 範例 |

## 注意事項

這些 skills 是從第三方 upstream 直接複製到本專案 staging 目錄。移植到 `.claude/skills/`、`.opencode/skills/` 或其他 agent runtime 前，仍建議依當前專案需求挑選子集，不要無差別全部安裝。
