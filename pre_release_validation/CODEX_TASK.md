# Visual Evidence Gateway v0.5.0 實機驗收任務指引

本任務用於驗收準備公開發布的 MCP 專案。請在目前的電腦上實際完成安裝、執行驗證、記錄數據，修正可安全處理的問題，再重新測試。

## 核心驗收目標

確認 Visual Evidence Gateway v0.5.0 是否具備發布條件：

1. 預設呼叫路徑是否確實為本機 Codex CLI + ChatGPT 登入 + `gpt-5.6-luna`；
2. 是否會在未告知的情況下切換至 API Key 計費、預設模型、verifier 或 fallback；
3. 一鍵安裝、MCP 註冊、實際像素探針及 `vision.inspect` 呼叫是否正常；
4. UI、OCR、圖表、前後比較、長圖及提示注入樣本是否確實通過測試；
5. README 的宣傳是否超出現有證據；
6. 發布套件是否包含個人路徑、憑證、執行狀態、快取或建置產生的多餘檔案。

## 執行規則

- 先閱讀 `pre_release_validation/README.md`、`README.md`、`AUDIT_REPORT.md` 和 `TEST_REPORT.md`。
- 不得讀取、輸出、複製或提交 `~/.codex/auth.json` 的內容。
- 不得建立或使用 API Key。若目前不是透過 ChatGPT 登入，停止並回報 P0 失敗。
- 不得為了通過測試而開啟 verifier/fallback、允許 CLI 使用預設模型，或放寬唯讀與停用工具的規則。
- 不得將模擬後端的結果當成實際 Luna 結果。
- 可以修改目前儲存庫內的程式碼、測試及文件，但改動應以完成修正所需的範圍為限。
- 每次修正後，必須重新執行相關測試及完整的發布檢查。

## 必須執行

在儲存庫根目錄執行：

```bash
python pre_release_validation/run_validation.py --runs 5 --host-mcp
```

接著執行：

```bash
python -m compileall -q src tests scripts pre_release_validation
python -m pytest
python scripts/audit_release.py
python scripts/benchmark_local.py
python scripts/verify_artifacts.py dist
codex login status
codex mcp list
visual-evidence-gateway-healthcheck --check-connectivity --json
visual-evidence-gateway-probe --backend primary --json
```

若使用 Windows，再執行以下命令並記錄結果：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -WhatIf
```

若腳本不支援 `-WhatIf`，不得將結果記為通過。請先審查腳本，再使用乾淨的測試帳號或隔離目錄實際執行安裝。

## MCP 主程式整合測試

1. 確認 `codex mcp list` 中存在 `visual-evidence-gateway`。
2. 在 Codex TUI 或 IDE 中使用 `/mcp`，確認可看到 `vision.inspect`。
3. 透過 MCP 工具讀取 `pre_release_validation/results/fixtures/text.png`，問題為：
   `只回傳圖片中的 RELEASE CODE，並提供證據位置。`
4. 回報工具原始結構中的 `status`、`evidence.image_index`、`verified_by` 和 `uncertainty`，不要輸出本機絕對路徑。

## 比較測試

使用同一部電腦、同一個帳號及同一張圖片比較：

- A：透過 Visual Evidence Gateway 的 `vision.inspect`；
- B：直接使用 Codex 原生附圖功能，並明確指定 `gpt-5.6-luna`。

至少比較以下項目：

- 答案是否正確；
- 端到端耗時；
- 輸出長度；
- 是否提供結構化證據、圖片索引及不確定性；
- 是否具備路徑授權、快取、提示注入最終檢查，以及失敗時拒絕回傳的機制。

不要預設 A 的視覺準確率較高。Visual Evidence Gateway 的核心假設是系統契約與跨主代理重用能力較強；若 B 較快或同樣準確，應如實記錄。

## 最終輸出

必須產生並填寫：

```text
pre_release_validation/results/REAL_WORLD_TEST_REPORT.md
pre_release_validation/results/validation-result.json
```

最終判定只能是 `PASS`、`CONDITIONAL PASS` 或 `FAIL`。請列出：

- 已通過的 P0；
- 未通過的 P0；
- P1 限制；
- 實測 Luna latency median/p95/min/max；
- 六類視覺樣本通過率；
- 與原生方案的比較結果；
- 完成的修正及重新驗證所用的命令；
- 目前可寫入公開 README 的宣傳文字；
- 目前必須刪除或降低主張強度的宣傳文字。
