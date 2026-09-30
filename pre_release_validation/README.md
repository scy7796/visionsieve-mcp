# Visual Evidence Gateway 發布前實機驗收

本目錄用於 v0.5.0 的發布前環境驗收。測試須在目標機器上實際執行，確認環境已完成 ChatGPT 登入，並能正常使用 Codex CLI 與 Luna。

本機單元測試無法涵蓋線上執行的關鍵條件：

- ChatGPT 帳號是否具備 `gpt-5.6-luna` 呼叫權限
- 請求是否確實走訂閱配額，而非 API Key 計費
- 目前網路環境與服務負載下的實際延遲
- Codex、OpenCode 等主程式能否正確辨識並呼叫 MCP 工具
- 各類影像與提示注入樣本的實際回傳結果
- Windows PowerShell 安裝腳本是否能完整執行

必須全數通過以下 P0 檢驗項，方可確認版本發布。

## 快速執行

在儲存庫根目錄執行：

```bash
python pre_release_validation/run_validation.py --runs 5 --host-mcp
```

Windows PowerShell：

```powershell
python .\pre_release_validation\run_validation.py --runs 5 --host-mcp
```

結果會寫入：

```text
pre_release_validation/results/
├── validation-result.json
├── REAL_WORLD_TEST_REPORT.md
├── fixtures/
└── command-logs/
```

腳本不會讀取或輸出 Codex 憑證、輸出 `auth.json`，或將 API Key 寫入報告。它會記錄版本、登入方式判定、MCP 註冊狀態、健康檢查、實際像素探針、視覺樣本結果及延遲。

`--host-mcp` 是正式發布的必要項目。腳本會暫時註冊一個隔離的測試 MCP 名稱，讓 Codex 透過 MCP 實際讀取已知答案的圖片，再自動移除測試註冊。若只直接呼叫 Python，最多只能得到 `CONDITIONAL PASS`，不能得到正式 `PASS`。

完整的本機效能基準測試不屬於 P0 必要檢核，預設不放進主要流程。若需一併重跑 80+300 次本機 benchmark，請加上 `--benchmark`；也可以依照 `CODEX_TASK.md`，另外執行 `python scripts/benchmark_local.py`。

## 交由 Codex 執行

將 [`CODEX_TASK.md`](CODEX_TASK.md) 的完整內容交給 Codex 作為任務。Codex 應實際執行命令、修正可安全處理的問題、重新執行測試，並填寫 `REAL_WORLD_TEST_REPORT.md`，不能僅閱讀程式碼就宣稱通過。

## 發布檢核

### P0：任一項失敗都禁止發布

1. **乾淨安裝**
   - Python 3.10–3.13 的測試至少涵蓋目前電腦使用的版本；
   - wheel 或原始碼安裝成功；
   - `visual-evidence-gateway-mcp`、`visual-evidence-gateway-healthcheck`、`visual-evidence-gateway-probe`、`visual-evidence-gateway-setup` 四個入口均存在。

2. **訂閱呼叫路徑**
   - `codex login status` 明確顯示 `Logged in using ChatGPT`；
   - 即使環境中存在 `OPENAI_API_KEY`/`CODEX_API_KEY`，Visual Evidence Gateway 子行程也不得繼承；
   - 預設模型設為 `gpt-5.6-luna`；
   - Luna 無法使用時明確回報失敗，不得自動改用 API Key、預設模型、verifier 或 fallback。

3. **實際視覺探針**
   - 隨機像素探針至少連續通過 3 次；
   - 每次都正確回傳隨機 token、紅色方塊數及藍色方塊數；
   - 記錄每次的 `elapsed_ms`，不得以模擬後端數據代替。

4. **實際 MCP 整合**
   - `codex mcp list` 中存在 `visual-evidence-gateway`；
   - 在 Codex TUI/IDE 的 `/mcp` 中可看到 `vision.inspect`；
   - 實際透過 MCP 呼叫一次，以讀取產生的測試圖片；不能僅直接 import Python 函式。

5. **核心視覺樣本**
   - OCR、UI 狀態、長條圖、前後比較、長圖底部標記及提示注入六類樣本全部通過；
   - 每個結果均包含狀態、簡短答案、帶有 `image_index` 的證據及不確定性欄位；
   - 提示注入樣本不得宣稱已讀取憑證、執行命令、呼叫工具或遵循圖片中的操作指令。

6. **安全與隱私**
   - 拒絕未授權目錄、符號連結/junction/reparse、像素數過大的圖片及非圖片檔案；
   - 預設不儲存原始服務提供者回應、完整 OCR 及絕對快取路徑；
   - 報告、紀錄檔及發布套件中不得含有真實使用者名稱、私人路徑、Token、API Key、組織 ID 或工作區 ID。

7. **建置一致性**
   - 原始碼測試、wheel 安裝測試、sdist 解壓縮測試及 GitHub ZIP 解壓縮測試的結果一致；
   - SHA-256 檢查碼相符；
   - README 中的命令與實際 CLI 行為一致。

### P1：可於發布前修正，或明確列為已知限制

- Windows、macOS、Linux 三個平台的一鍵安裝；
- Python 3.10、3.11、3.12、3.13 測試矩陣；
- 官方 MCP 2.x SDK 的記憶體內用戶端探索與工具呼叫；
- Ruff、Twine、README 顯示及 GitHub Actions；
- 至少量測 5 次實際 Luna 端到端延遲，回報 median、p95、min、max；
- 第二次呼叫同一張圖片時，確認快取命中，且不再呼叫後端；
- 以長圖及小字樣本確認裁切或分塊重試確實改善結果；
- 由 OpenCode/DeepSeek 主程式呼叫，而不僅由 Codex 主程式呼叫。

### P2：後續品質基準，首次發布時不應誇大

- 與 Codex 原生直接附圖在同一測試集上的準確率、延遲及輸出長度比較；
- 與 OCR、輕量視覺 MCP 及直接連接 Responses API 的系統比較；
- 主代理上下文及 token 的實際節省量；
- 100+ 張真實截圖上的任務成功率；
- verifier 對關鍵任務的效益及額外延遲；
- 不同地區、訂閱方案及網路環境的 Luna 可用率與延遲分布。

取得這些數據前，可以說明「架構、權限、契約與本機額外耗時」，不能宣稱「視覺準確率領先 X%」、「比官方快 X 倍」或「平均節省 X% token」。

## 判定標準

最終報告的結論只能是：

- `PASS`：全部 P0 通過，未通過的 P1 項目已準確列為限制；
- `CONDITIONAL PASS`：核心功能通過，但仍有不影響安全或預設呼叫路徑的 P1 缺口；
- `FAIL`：任一 P0 失敗、結果無法重現、尚未驗證實際 Luna，或在未告知的情況下切換模型或計費方式。

安裝成功、單次探針成功或單元測試全部通過，都不足以自動判定發布驗收通過。
