# Django Blog 專案

本專案是一個基於 **Django** 和 **Django REST Framework** 開發的部落格應用程式，提供使用者管理、文章管理及密碼重設功能。

## 功能特色  
- **帳號管理**：註冊、登入、登出、個人資料查看與修改  
- **文章管理**：新增、刪除、修改、查看、分類、搜尋、評論、收藏  
- **密碼管理**：提供密碼修改與重設功能  

## 系統需求  
- **作業系統**：Windows / macOS / Linux  
- **Python**：版本 3.12 以上  
- **Django**：版本 5.1.1  
- **依賴套件**：根據 `pyproject.toml` 包含以下主要套件：  
  ```plaintext
  django==5.1.1  
  djangorestframework==3.15.2  
  django-ckeditor==6.7.1  
  django-cors-headers==4.4.0  
  pillow==10.4.0  
  python-dotenv==1.0.1  
  django-countries==7.6.1  
