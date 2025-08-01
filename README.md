# Wan2.1 專案內容及功能

## 專案目錄結構
```
Wan2.1/
├── main/
│   ├── __init__.py
│   ├── approve_button.py
│   ├── export_button.py
│   ├── prompt_initial.py
│   ├── prompt_optimize.py
│   ├── refresh_button.py
│   ├── Wan2.1.md
├── wan/
│   ├── configs/
│   ├── distributed/
│   ├── modules/
│   ├── utils/
├── assets/
├── cache/
├── examples/
├── output/
├── tests/
├── Wan2.1-VACE-1.3B/
```

## 主要功能

### 1. 提示詞生成與優化
- **初始化提示詞**：
  - 使用 `PromptInitial` 函數，根據輸入的圖片生成詳細描述。
  - 支援多張圖片的分析，並生成整合的提示詞。
- **優化提示詞**：
  - 使用 `PromptOptimize` 函數，根據輸入的提示詞進行語意優化，生成更完整、更具表現力的提示詞。

### 2. 影片生成
- **生成影片**：
  - 使用 `generate` 方法，基於提示詞、參考圖片及其他參數生成影片。
  - 支援多種參數設定，如移動幅度、採樣步數、上下文關聯性等。
- **影片片段儲存**：
  - 使用 `approve_btn` 函數，將生成的影片片段儲存至指定目錄。
- **匯出完整影片**：
  - 使用 `export_btn` 函數，將所有儲存的影片片段合併並匯出為完整影片。

### 3. 使用者介面
- **Gradio UI**：
  - 提供直觀的使用者介面，包含影片上傳、參考圖片上傳、提示詞輸入及參數調整。
  - 支援按鈕操作，如初始化提示詞、優化提示詞、生成影片、儲存片段及匯出影片。

### 4. 多模型支援
- 支援多種模型（如 `vace-14B` 和 `vace-1.3B`），可根據需求選擇不同的模型進行推理。

## 主要檔案與功能

| **檔案**                     | **功能**                                                                 |
|------------------------------|--------------------------------------------------------------------------|
| `main.py`                    | 主程式入口，負責初始化模型、建立 UI 並處理按鈕回調。                     |
| `prompt_initial.py`          | 根據輸入圖片生成初始提示詞。                                                |
| `prompt_optimize.py`         | 優化提示詞，生成更完整的敘述。                                              |
| `approve_button.py`          | 儲存影片片段至指定目錄。                                                   |
| `export_button.py`           | 合併影片片段並匯出完整影片。                                               |
| `refresh_button.py`          | 清空影片展示區並顯示提示訊息。                                             |

## 使用方法

### 1. 啟動專案
執行以下指令啟動 Gradio UI：
```bash
python main.py
```

### 2. 使用功能
- **上傳影片及參考圖片**：在 UI 中上傳影片及最多三張參考圖片。
- **輸入提示詞**：輸入正向及負向提示詞。
- **調整參數**：設定移動幅度、採樣步數、上下文關聯性等參數。
- **生成影片**：點擊 `Run` 按鈕生成影片。
- **儲存片段**：點擊 `✅ 儲存當前片段` 按鈕儲存影片片段。
- **匯出完整影片**：點擊 `📤 匯出完整影片` 按鈕匯出影片。

## 技術細節
- **模型推理**：使用 `WanVace` 或 `WanVaceMP` 進行影片生成。
- **影片處理**：使用 `moviepy` 合併影片片段並匯出。
- **UI 框架**：基於 `Gradio` 提供互動式使用者介面。

此專案適合用於生成高品質影片，並支援多種提示詞生成與優化功能，提供直觀的使用者介面以提升使用體驗。