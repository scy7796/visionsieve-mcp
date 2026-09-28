# Visual Evidence Gateway 繁體中文說明

完整繁體中文說明已經移至儲存庫根目錄的 [`README.md`](../README.md)，其中包括：

- 一鍵安裝與真實像素驗收；
- 為何相比直接貼圖、OCR、一般視覺 API 包裝器與 Computer Use 更適合文字代理；
- 與 Codex 官方原生看圖的正面對比，以及為何 DeepSeek 主代理 + Luna 視覺專家更合適；
- 本地橋接開銷實測與真實 Luna `elapsed_ms` 探針；
- Luna 訂閱優先調用契約；
- 最小上下文、裁剪/分塊重試、Schema 校驗與提示注入防護；
- 安全邊界、配置、故障排查、升級與卸載。

## 發布前真實驗收

公開發布前執行 `python pre_release_validation/run_validation.py --runs 5 --host-mcp`。本地測試只能證明代碼契約，不能證明帳號權限、訂閱路由、真實 Luna 延遲、宿主級 MCP 調用或跨平台安裝。詳見 `pre_release_validation/README.md` 與 `claims-matrix.md`。
