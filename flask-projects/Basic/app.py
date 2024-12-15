# Basic/app.py
# 主應用入口檔案，初始化 Flask 應用與擴展，並註冊路由

from flask import Flask, flash, redirect, render_template, request, session, url_for
from models import User  # 修正為正確的相對匯入
from flask_jwt_extended import JWTManager
from models import db, bcrypt
from routes import api
from config import Config
from flask_mail import Mail

# 初始化 Flask 應用
app = Flask(__name__)
app.config.from_object(Config)  # 載入配置

# 初始化擴展
db.init_app(app)  # 資料庫
bcrypt.init_app(app)  # 密碼雜湊處理
jwt = JWTManager(app)  # JWT 驗證
mail = Mail(app)  # 初始化 Flask-Mail
app.register_blueprint(api, url_prefix='/api')  # 註冊 API 路由

# 網頁路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout_page():
    session.pop('logged_in', None)  # 清除登入狀態
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash("您已成功登出！", "info")
    return render_template('logout.html')  # 登出頁模板

@app.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>')
def reset_password_page(token):
    return render_template('reset_password.html', token=token)

@app.route('/profile')
def profile_page():
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入！", "danger")
        return redirect(url_for('login_page'))
    user = db.session.get(User, user_id)  # 使用 Session.get()
    if not user:
        flash("使用者不存在！", "danger")
        return redirect(url_for('login_page'))
    return render_template('profile.html', user=user)

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile_page():
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入！", "danger")
        return redirect(url_for('login_page'))
    user = db.session.get(User, user_id)  # 使用 Session.get()
    if not user:
        flash("使用者不存在！", "danger")
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        data = request.form
        if "phone" in data:
            user.phone = data['phone']
        if "bio" in data:
            user.bio = data['bio']
        if "address" in data:
            user.address = data['address']
        db.session.commit()
        flash("個人資料更新成功！", "success")
        return redirect(url_for('profile_page'))

    return render_template('edit_profile.html', user=user)

# 管理員路由
@app.route('/admin')
def admin_page():
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入！", "danger")
        return redirect(url_for('login_page'))
    user = db.session.get(User, user_id)  # 使用 Session.get()
    if not user:
        flash("使用者不存在！", "danger")
        return redirect(url_for('login_page'))
    if not user.is_admin:
        flash("權限不足！", "danger")
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/admin/user/<int:user_id>')
def admin_user_page(user_id):
    user = db.session.get(User, user_id)  # 使用 Session.get()
    if not user:
        flash("使用者不存在！", "danger")
        return redirect(url_for('admin_page'))
    return render_template('admin_user.html', user=user)

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
def admin_delete_user(user_id):
    user = db.session.get(User, user_id)  # 使用 Session.get()
    if not user:
        flash("使用者不存在！", "danger")
        return redirect(url_for('admin_page'))
    db.session.delete(user)
    db.session.commit()
    flash("使用者已刪除！", "success")
    return redirect(url_for('admin_page'))

@app.route('/admin/user/<int:user_id>/toggle-active', methods=['POST'])
def admin_toggle_active_user(user_id):
    user = db.session.get(User, user_id)  # 使用 Session.get()
    if not user:
        flash("使用者不存在！", "danger")
        return redirect(url_for('admin_page'))
    user.is_active = not user.is_active
    db.session.commit()
    flash("使用者已更新！", "success")
    return redirect(url_for('admin_page'))

@app.route('/admin/user/<int:user_id>/toggle-admin', methods=['POST'])
def admin_toggle_admin_user(user_id):
    user = db.session.get(User, user_id)  # 使用 Session.get()
    if not user:
        flash("使用者不存在！", "danger")
        return redirect(url_for('admin_page'))
    user.is_admin = not user.is_admin
    db.session.commit()
    flash("使用者已更新！", "success")
    return redirect(url_for('admin_page'))

# 建構管理者帳號
@app.cli.command('create-admin')
def create_admin():
    username = input("輸入管理者使用者名稱: ")
    email = input("輸入管理者電子郵件: ")
    password = input("輸入管理者密碼: ")

    admin = User(username=username, email=email, is_admin=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print("管理者帳號已建立！")

# 初始化資料庫
@app.cli.command('init-db')
def init_db():
    with app.app_context():
        db.create_all()
    print("資料庫已初始化！")

# 啟動應用
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 建立資料庫
    app.run(debug=True)  # 啟動開發伺服器