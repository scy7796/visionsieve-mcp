# Visual Evidence Gateway 說明

完整文件請參閱根目錄的 [`README.md`](../README.md)。

這套工具為以文字為主的 Agent（如 DeepSeek 或 OpenCode）提供輕量的視覺通道。當任務需要辨識截圖或圖表時，Agent 可以透過一個唯讀的 MCP 工具呼叫 Luna，取得精簡、結構化的關鍵證據，避免將完整圖片或長篇 OCR 文字放進對話上下文。

核心機制包括：

- 呼叫時鎖定 ChatGPT 訂閱配額下的 Luna；未經授權，不切換至付費 API 或其他模型
- 嚴格限制上下文長度，支援大圖裁切、分塊與重試，並執行 Schema 與提示注入防護
- 提供本機呼叫額外耗時的量測與實際延遲探針

## 發布前驗收

正式發布前，請在已登入環境執行實機驗收：

```bash
python pre_release_validation/run_validation.py --runs 5 --host-mcp
```

本機單元測試可檢查程式碼的語法與邏輯，但無法證明帳號具有 Luna 權限、實際網路延遲符合需求，或 MCP 能被主程式正確載入。測試細節與驗收標準請參閱 `pre_release_validation/README.md` 與 `claims-matrix.md`。
