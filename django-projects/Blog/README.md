# 📝 Django Blog 專案

本專案是一個基於 **Django** 和 **Django REST Framework** (DRF) 開發的 **部落格系統**，提供完整的 **帳號管理、文章管理及密碼重設** 功能，並支援 **Docker 容器化部署**，確保可擴展性與部署便利性。

---

## 🎯 功能特色

### 🔹 **帳號管理**
✅ 註冊、登入、登出
✅ 個人資料查看與修改

### 🔹 **文章管理**
✅ 文章 **新增、編輯、刪除、分類、搜尋**
✅ 支援 **評論**、**收藏**

### 🔹 **密碼管理**
✅ **修改密碼** 與 **重設密碼** 機制

---

## 🚀 如何啟動專案 (本地環境)

### 1️⃣ **安裝與設定**
請確保已安裝 **Python 3.8+**，然後執行：

```sh
# 確認已安裝 Poetry
poetry --version

# 克隆此專案到本地端
git clone https://github.com/zoelinsg/Django-Projects.git

# 進入專案目錄
cd Basic1

# 使用 Poetry 安裝依賴
poetry install

# 建立並啟動虛擬環境
poetry shell
```

### 2️⃣ **進行資料庫遷移**

```sh
python manage.py makemigrations
python manage.py migrate
```

### 3️⃣ **創建超級用戶**

```
sh
複製編輯
python manage.py createsuperuser

```

### 4️⃣ **啟動開發伺服器**

```sh
python manage.py runserver

```

伺服器啟動後，請開啟瀏覽器進入：

```cpp
http://127.0.0.1:8000/
```

---

## 🐳 使用 Docker 啟動 (可選)

若要使用 **Docker** 方式執行：

```sh
docker-compose up -d --build
```

---

## 🌐 線上服務

🔹 **網站開放時間**: **平日 11:00 - 19:00（GMT+8）**，其他時間請聯繫 **zoelin.sg@gmail.com** 申請訪問權限。

| 項目名稱 | 連結 |
| --- | --- |
| **Django 部落格系統** | [進入網站](https://zoe-blog.sunflowx.com/) |
