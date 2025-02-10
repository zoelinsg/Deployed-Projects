# 🚀 已成功部署的網站

本專案已成功部署至 **AWS EC2**，使用 **Django RESTful API** 作為後端，並透過 **Docker** 容器化管理，搭配 **Nginx + Certbot** 進行 HTTPS 配置，以確保安全性與效能最佳化。並使用 **Poetry** 進行 Python 套件管理，提高開發與部署效率。

## 🔧 技術架構

- **虛擬環境管理**: 使用 Poetry 安裝與管理 Python 套件
- **後端**: Django RESTful API (提供資料與 API 服務)
- **前端**: Django Templates (HTML, CSS, JavaScript)
- **容器化技術**: Docker、Docker Compose
- **伺服器架構**: AWS EC2 (Ubuntu)
- **網域與憑證**: AWS Route 53、Nginx + Certbot (SSL)

## 📌 部署流程

### 1️⃣ AWS EC2 設定
- 在 **AWS EC2** 建立並配置 **Ubuntu 伺服器**
- 設定防火牆 (開啟 **80, 443, 8000** 端口)
- 更新系統並安裝必要工具：
  ```sh
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y python3-pip docker.io docker-compose certbot
  ```

- 透過 SSH 連線至 EC2 主機

### 2️⃣ 環境與容器設定

- 使用 **Poetry** 安裝 Python 依賴：
    
    ```sh
    poetry install
    ```
    
- 撰寫 **Dockerfile** 來建置 Django API 環境
- 設定 **docker-compose.yaml** 來管理多個容器
- 使用 **entrypoint.sh** 來處理容器啟動邏輯
- 打包專案並啟動容器：
    
    ```sh
    docker-compose up -d --build
    ```
    

### 3️⃣ Nginx 反向代理 & HTTPS 設定

- 配置 **Nginx** 作為反向代理，將流量轉發至 Django API
- 透過 **Certbot** 申請並自動更新 **SSL 憑證**
    
    ```sh
    sudo certbot --nginx -d yourdomain.com    
    ```
    

### 4️⃣ 設定 AWS Domain

- 透過 **AWS Route 53** 綁定自訂網域
- 設定 DNS 紀錄，將網域指向 EC2 Public IP

## 📂 主要文件說明

| 檔案名稱 | 作用 |
| --- | --- |
| `Dockerfile` | 定義 Django API 環境 |
| `docker-compose.yaml` | 服務編排與容器管理 |
| `entrypoint.sh` | 容器啟動時的初始化指令 |
| `nginx.conf` | Nginx 反向代理設定 |
| `pyproject.toml` | Poetry 專案與依賴配置 |

## 📖 參考資料

- [Django REST Framework 官方文件](https://www.django-rest-framework.org/)
- [AWS EC2 部署指南](https://aws.amazon.com/ec2/)
- [Docker 官方文件](https://docs.docker.com/)
- [Poetry 官方文件](https://python-poetry.org/docs/)

## 🌐 線上服務

🔹 **網站開放時間**: **平日 11:00 - 19:00（GMT+8）**，其他時間請聯繫 **zoelin.sg@gmail.com** 申請訪問權限。

| 項目名稱 | 連結 |
| --- | --- |
| Django 部落格系統 | [🔗 進入網站](https://zoe-blog.sunflowx.com/) |
| Django 電商網站 | [🔗 進入網站](https://zoe-ecommerce.sunflowx.com/) |
| Django 圖書館系統 | [🔗 進入網站](https://zoe-library.sunflowx.com/) |
