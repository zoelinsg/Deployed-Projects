# Basic/config.py
# 配置檔案，包含應用的基本設定

from dotenv import load_dotenv
import os

# 載入 .env 文件
load_dotenv()

class Config:
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # 安全密鑰，用於加密
    SQLALCHEMY_DATABASE_URI = 'sqlite:///basic.db'  # 資料庫 URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 關閉追蹤修改（提升效能）

    # Flask-Mail 配置
    MAIL_SERVER = 'smtp.gmail.com'  # 郵件伺服器
    MAIL_PORT = 587  # 郵件伺服器連接埠
    MAIL_USE_TLS = True  # 啟用 TLS 加密
    MAIL_USERNAME = os.environ.get('ZOE_EMAIL_HOST_USER')  # 從環境變數讀取郵件使用者名稱
    MAIL_PASSWORD = os.environ.get('ZOE_EMAIL_HOST_PASSWORD')  # 從環境變數讀取郵件密碼