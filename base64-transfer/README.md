# 使用 Base64 將 7z 從 Windows 11 傳送到 Linux

這個流程適合只能傳送或貼上純文字、無法直接傳送二進位檔案的環境。Windows 11 先把 `frontend-skill.7z` 編碼為 `transfer.txt`，並把原始壓縮檔的 SHA-256 儲存到 `frontend-skill.7z.sha256.txt`；Linux 收到兩個文字檔後，再還原壓縮檔並驗證內容是否完全一致。

## 1. Windows 11：轉成 Base64 並儲存 SHA-256

將 `frontend-skill.7z` 放在目前目錄，使用 PowerShell 執行以下一行指令：

```powershell
$archive="frontend-skill.7z"; [Convert]::ToBase64String([IO.File]::ReadAllBytes($archive),[Base64FormattingOptions]::InsertLineBreaks) | Set-Content -Encoding ascii transfer.txt; (Get-FileHash $archive -Algorithm SHA256).Hash.ToLowerInvariant() | Set-Content -Encoding ascii frontend-skill.7z.sha256.txt
```

指令會產生兩個要傳送到 Linux 的純文字檔：

```text
transfer.txt
frontend-skill.7z.sha256.txt
```

- `transfer.txt`：`frontend-skill.7z` 的 Base64 內容。
- `frontend-skill.7z.sha256.txt`：原始 `frontend-skill.7z` 的 SHA-256。

## 2. 將文字檔傳送到 Linux

把以下兩個檔案放進 Linux 的同一個目錄：

```text
transfer.txt
frontend-skill.7z.sha256.txt
```

## 3. Linux：還原 7z 並驗證 SHA-256

在該目錄執行以下一行指令：

```bash
base64 --ignore-garbage --decode transfer.txt > frontend-skill.7z && printf '%s  %s\n' "$(tr -d '\r\n' < frontend-skill.7z.sha256.txt)" frontend-skill.7z | sha256sum --check -
```

`--ignore-garbage` 會忽略 Windows 產生的 CRLF 換行字元。驗證成功時會顯示：

```text
frontend-skill.7z: OK
```

如果顯示 `FAILED` 或指令回傳非零狀態，代表 Base64 文字、SHA-256 檔案或還原後的壓縮檔不一致；不要解壓或使用該檔案，應重新傳送。

驗證成功後即可解壓縮：

```bash
7z x frontend-skill.7z
```

## 流程摘要

```text
Windows 11
frontend-skill.7z
        ├─ Base64 ──> transfer.txt
        └─ SHA-256 ─> frontend-skill.7z.sha256.txt
                         │
                         ▼
                 傳送兩個純文字檔
                         │
                         ▼
Linux
transfer.txt ── Base64 decode ──> frontend-skill.7z
                                      │
frontend-skill.7z.sha256.txt ─────────┴─> sha256sum 驗證
```