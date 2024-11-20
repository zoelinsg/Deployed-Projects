from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

# 掛載靜態文件的路徑，將/static對應到本地的static資料夾
app.mount("/static", StaticFiles(directory="static"), name="static")

# 設定模板文件夾的位置，用於處理HTML模板
templates = Jinja2Templates(directory="templates")

# 定義儲存部落格資料的檔案名稱
BLOG_FILE = "blog.json"

# 如果部落格資料檔案不存在，則創建一個空的JSON檔案
if not os.path.exists(BLOG_FILE) or os.stat(BLOG_FILE).st_size == 0:
    with open(BLOG_FILE, "w") as f:
        json.dump([], f)

# 讀取部落格資料的函式，從JSON檔案中讀取
def read_blog_data():
    with open(BLOG_FILE, "r") as f:
        return json.load(f)

# 寫入部落格資料的函式，將更新後的資料寫入JSON檔案
def write_blog_data(data):
    with open(BLOG_FILE, "w") as f:
        json.dump(data, f)

# 定義首頁路由，顯示所有部落格文章
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    blogs = read_blog_data()  # 讀取所有部落格資料
    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})

# 定義文章詳細內容的路由，根據post_id顯示指定文章
@app.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int):
    blogs = read_blog_data()  # 讀取所有部落格資料
    post = blogs[post_id] if 0 <= post_id < len(blogs) else None
    return templates.TemplateResponse("post.html", {"request": request, "post": post})

# 定義創建新文章表單的路由，顯示表單頁面
@app.get("/create_post", response_class=HTMLResponse)
async def create_post_form(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})

# 定義處理創建新文章的路由，從表單接收資料並儲存
@app.post("/create_post")
async def create_post(title: str = Form(...), content: str = Form(...)):
    blogs = read_blog_data()  # 讀取現有部落格資料
    blogs.append({"title": title, "content": content})  # 新增文章
    write_blog_data(blogs)  # 將更新後的資料寫入JSON檔案
    return RedirectResponse("/", status_code=303)

# 定義刪除文章的路由，根據post_id刪除指定文章
@app.post("/delete_post/{post_id}")
async def delete_post(post_id: int):
    blogs = read_blog_data()  # 讀取所有部落格資料
    if 0 <= post_id < len(blogs):
        blogs.pop(post_id)  # 刪除文章
        write_blog_data(blogs)  # 更新後寫入JSON檔案
    return RedirectResponse("/", status_code=303)

# 新增修改文章的表單路由
@app.get("/edit_post/{post_id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int):
    blogs = read_blog_data()  # 讀取部落格資料
    post = blogs[post_id] if 0 <= post_id < len(blogs) else None
    if post:
        return templates.TemplateResponse("edit_post.html", {"request": request, "post_id": post_id, "post": post})
    else:
        return RedirectResponse("/", status_code=303)

# 處理修改文章的路由
@app.post("/edit_post/{post_id}")
async def edit_post(post_id: int, title: str = Form(...), content: str = Form(...)):
    blogs = read_blog_data()  # 讀取現有部落格資料
    if 0 <= post_id < len(blogs):
        blogs[post_id] = {"title": title, "content": content}  # 更新文章內容
        write_blog_data(blogs)  # 將更新後的資料寫入JSON檔案
    return RedirectResponse("/", status_code=303)
