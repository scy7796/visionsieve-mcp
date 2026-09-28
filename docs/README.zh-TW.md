# Visual Evidence Gateway 說明

完整文件請參閱根目錄的 [`README.md`](../README.md)。

這套工具主要是為文字為主的 Agent（如 DeepSeek 或 OpenCode）設計的輕量視覺通道。當任務需要辨識截圖或圖表時，Agent 可以透過一個唯讀的 MCP 工具調用 Luna，取回少量的結構化關鍵證據，而不需要把整張圖或長篇 OCR 文本直接塞進對話上下文。

核心機制包括：
- 調用時鎖定 ChatGPT 訂閱配額下的 Luna，不在未授權時退回付費 API 或替換模型
- 嚴格限制上下文長度，支援大圖裁切、分塊與重試，並執行 Schema 與提示注入防護
- 提供本地調用損耗與實際延遲探針

## 發布前驗收

正式發布前，請在已登入環境執行實機驗收：

```bash
python pre_release_validation/run_validation.py --runs 5 --host-mcp
```

本地單元測試只能確認代碼沒有語法或邏輯錯誤，無法證明帳號的 Luna 權限、實際網路延遲以及 MCP 能否被宿主正確載入。測試細節與驗收標準可參考 `pre_release_validation/README.md` 與 `claims-matrix.md`。
