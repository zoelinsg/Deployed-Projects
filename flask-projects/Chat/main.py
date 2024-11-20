from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# 建立 Flask 應用程式實例
app = Flask(__name__)

# 設定 Flask 的密鑰，用於處理 session 資料的加密
app.config["SECRET_KEY"] = "hjhjsdahhds"

# 建立 SocketIO 實例，與 Flask 應用整合
socketio = SocketIO(app)

# 定義全域變數 rooms，儲存所有的房間資料
rooms = {}

# 定義函式以生成唯一的房間代碼
def generate_unique_code(length):
    while True:
        code = ""
        # 隨機生成指定長度的代碼
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        # 確保生成的代碼不與現有房間重複
        if code not in rooms:
            break
    
    return code

# 定義首頁路由，處理 GET 和 POST 請求
@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()  # 清空使用者的 session
    if request.method == "POST":
        # 從表單獲取使用者輸入的名稱和房間代碼
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # 如果沒有輸入名稱，返回錯誤
        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        # 如果選擇加入房間但沒有輸入房間代碼，返回錯誤
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        # 判斷使用者是創建房間還是加入房間
        room = code
        if create != False:
            # 如果是創建房間，生成唯一房間代碼並創建房間
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}  # 初始化房間成員數量和訊息
        elif code not in rooms:
            # 如果房間不存在，返回錯誤訊息
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        # 將房間代碼和使用者名稱儲存在 session 中
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))  # 重新導向到房間頁面

    return render_template("home.html")  # 返回首頁模板

# 定義房間頁面的路由
@app.route("/room")
def room():
    room = session.get("room")  # 從 session 中取得房間代碼
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))  # 如果房間不存在或無名稱，返回首頁

    # 返回房間頁面並顯示訊息
    return render_template("room.html", code=room, messages=rooms[room]["messages"])

# 處理收到的訊息
@socketio.on("message")
def message(data):
    room = session.get("room")  # 取得當前房間
    if room not in rooms:
        return 
    
    # 組合訊息內容，包括發送者名稱和訊息
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)  # 傳送訊息到指定房間
    rooms[room]["messages"].append(content)  # 將訊息添加到房間的訊息列表
    print(f"{session.get('name')} said: {data['data']}")  # 在伺服器端打印訊息

# 處理使用者連線事件
@socketio.on("connect")
def connect(auth):
    room = session.get("room")  # 取得房間代碼
    name = session.get("name")  # 取得使用者名稱
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)  # 加入房間
    send({"name": name, "message": "has entered the room"}, to=room)  # 發送使用者進入房間的通知
    rooms[room]["members"] += 1  # 增加房間成員數量
    print(f"{name} joined room {room}")  # 伺服器端打印訊息

# 處理使用者斷線事件
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")  # 取得房間代碼
    name = session.get("name")  # 取得使用者名稱
    leave_room(room)  # 離開房間

    if room in rooms:
        rooms[room]["members"] -= 1  # 減少房間成員數量
        if rooms[room]["members"] <= 0:
            del rooms[room]  # 如果房間沒有人，則刪除房間
    
    send({"name": name, "message": "has left the room"}, to=room)  # 傳送離開訊息到房間
    print(f"{name} has left the room {room}")  # 伺服器端打印訊息

# 主程式入口，啟動應用程式
if __name__ == "__main__":
    socketio.run(app, debug=True)
