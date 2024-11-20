from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dataclasses import dataclass
from typing import Dict
import uuid
import json

# 設定模板目錄為 "templates"
templates = Jinja2Templates(directory="templates")

@dataclass
class ConnectionManager:
    """管理 WebSocket 連線的類別"""
    def __init__(self) -> None:
        # 使用字典來儲存活躍的連線，key 為連線 id，value 為 WebSocket 物件
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket):
        """接受 WebSocket 連線並儲存"""
        await websocket.accept()
        # 產生唯一的連線 ID
        id = str(uuid.uuid4())
        self.active_connections[id] = websocket
        # 發送歡迎訊息給該連線的用戶
        await self.send_message(websocket, json.dumps({"isMe": True, "data": "Have joined!!", "username": "You"}))

    async def send_message(self, ws: WebSocket, message: str):
        """發送訊息給指定的 WebSocket 連線"""
        await ws.send_text(message)

    def find_connection_id(self, websocket: WebSocket):
        """根據 WebSocket 物件找到對應的連線 ID"""
        websocket_list = list(self.active_connections.values())
        id_list = list(self.active_connections.keys())
        # 找到該 WebSocket 在字典中的位置，並返回對應的 ID
        pos = websocket_list.index(websocket)
        return id_list[pos]

    async def broadcast(self, webSocket: WebSocket, data: str):
        """廣播訊息給所有連線，包括發送者"""
        decoded_data = json.loads(data)  # 解析來自客戶端的 JSON 訊息

        for connection in self.active_connections.values():
            is_me = False
            if connection == webSocket:
                is_me = True  # 標記訊息是由當前客戶端發送的

            # 發送訊息給每個已連線的客戶端
            await connection.send_text(json.dumps({
                "isMe": is_me, 
                "data": decoded_data['message'], 
                "username": decoded_data['username']
            }))

    def disconnect(self, websocket: WebSocket):
        """斷開 WebSocket 連線並移除其 ID"""
        id = self.find_connection_id(websocket)  # 根據 WebSocket 找到連線 ID
        del self.active_connections[id]  # 從活躍連線中移除該連線
        return id

# 創建 FastAPI 應用實例
app = FastAPI()

# 設定靜態檔案路徑，讓應用可以服務靜態檔案（例如：CSS、JS）
app.mount("/static", StaticFiles(directory="static"), name="static")

# 創建 ConnectionManager 實例
connection_manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
def get_room(request: Request):
    """返回首頁的 HTML 頁面"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/message")
async def websocket_endpoint(websocket: WebSocket):
    """處理 WebSocket 連線的端點"""
    # 接受客戶端連線
    await connection_manager.connect(websocket)

    try:
        while True:
            # 持續接收來自客戶端的訊息
            data = await websocket.receive_text()
            # 廣播該訊息給所有已連線的客戶端
            await connection_manager.broadcast(websocket, data)
    except WebSocketDisconnect:
        # 當客戶端斷開時，移除該連線
        id = connection_manager.disconnect(websocket)
        # 導向首頁
        return RedirectResponse("/")

@app.get("/join", response_class=HTMLResponse)
def get_room(request: Request):
    """返回加入房間的 HTML 頁面"""
    return templates.TemplateResponse("room.html", {"request": request})
