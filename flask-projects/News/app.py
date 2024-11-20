from flask import Flask, render_template, request
import requests
from config import NEWS_API_KEY  # 匯入 News API 金鑰

# 創建一個 Flask 應用程式實例
app = Flask(__name__)

# 首頁路由
@app.route("/")
def index():
    # 從 URL 查詢參數中獲取搜尋關鍵字，如果沒有則設為 "latest"
    query = request.args.get("query", "latest")
    
    # 使用 f-string 格式化 URL 來包含查詢關鍵字和 API KEY
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    
    try:
        # 發送 GET 請求以獲取新聞數據
        response = requests.get(url)
        response.raise_for_status()  # 檢查是否有 HTTP 錯誤
        news_data = response.json()  # 將回應轉換為 JSON 格式
        articles = news_data.get('articles', [])  # 從 JSON 中提取文章列表
        
        # 過濾掉來自 "Yahoo" 的新聞及標題包含 "removed" 的文章
        filtered_articles = [
            article for article in articles
            if "Yahoo" not in article["source"]["name"] and 'removed' not in article["title"].lower()
        ]
    except requests.exceptions.RequestException as e:
        # 在發生錯誤時返回空列表
        print(f"Error fetching news data: {e}")
        filtered_articles = []

    # 渲染 index.html 並傳遞文章列表和查詢字詞
    return render_template("index.html", articles=filtered_articles, query=query)

# 啟動應用程式
if __name__ == "__main__":
    app.run(debug=True)
