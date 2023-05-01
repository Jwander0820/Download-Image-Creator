# Download-Image-Creator

Download-Image-Creator 是一個簡單的 Python 應用，用於從 Bing 影像建立者網站下載圖片。該應用提供了一個簡單的 Web 介面，允許用戶通過提供圖片的 URL 或 token 來下載圖片。

## 功能
- 爬取指定的 Bing 影像建立者 URL 以獲取圖片
- 提供簡單的網頁介面，允許用戶輸入 URL 或 token 以及資料夾名稱來下載圖片
- 下載的圖片會儲存在指定的資料夾中
- 自動檢查是否已經訪問過 URL，避免重複下載
- 快捷功能 : Ctrl + V 自動貼上複製的內容並下載圖片(AutoPaste控制開關)
- 快捷功能 : 拖曳網址到網頁上，自動貼上網址並下載圖片(全域執行)


## 如何使用
### 1. 複製儲存庫
```commandline
git clone https://github.com/Jwander0820/Download-Image-Creator.git
```
### 2. 安裝所需的套件：
```commandline
pip install -r requirements.txt
```

### 3. 運行 Flask 應用
在終端中，切換到指定目錄並執行以下命令：
```commandline
python app.py
```

### 4. 執行
1. 打開瀏覽器，訪問 http://localhost:8080 以查看應用程序的主頁面。

2. 輸入有效的 URL 或 token，然後單擊 "Download Images" 按鈕以開始下載圖片。

3. 下載完成後，您將在主頁面上看到相應的消息。下載的圖片將保存在應用程序目錄下的 img 文件夾中。

### Ex. Windows .bat
1. 建議建置一個虛擬環境，安裝所需套件
2. 建立.bat檔，並寫入以下指令
   - call 其後填入虛擬環境的啟動檔
   - python 其後填入app.py路徑
3. 執行.bat檔會自動開啟網頁並啟動虛擬環境與Flask服務

```commandline
@echo off
start http://127.0.0.1:8080
call C:\Download-Image-Creator\venv\Scripts\activate
python C:\Download-Image-Creator\app.py
```

## 注意事項
- 下載圖片時請確保 URL 或 token 正確，否則應用程序可能無法正常運行。
- 應用程序捕捉可能的錯誤並在主頁面上顯示錯誤消息，但可能無法處理所有情況。