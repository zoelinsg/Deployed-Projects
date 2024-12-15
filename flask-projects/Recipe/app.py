import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from models import Recipe, User  # 修正為正確的相對匯入
from models import db, bcrypt
from routes import api
from config import Config
from flask_mail import Mail

# 初始化 Flask 應用
app = Flask(__name__)
app.config.from_object(Config)  # 載入配置
app.config['UPLOAD_FOLDER'] = 'static/images'  # 設定上傳文件夾
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # 設定允許的文件類型

# 初始化擴展
db.init_app(app)  # 資料庫
bcrypt.init_app(app)  # 密碼雜湊處理
mail = Mail(app)  # 初始化 Flask-Mail
app.register_blueprint(api, url_prefix='/api')  # 註冊 API 路由

# 檢查文件類型是否允許
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 網頁路由
# 首頁(食譜列表)
@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

# 註冊
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        data = request.form
        if not all(k in data for k in ('username', 'email', 'password')):
            flash("所有欄位為必填！", "danger")
            return redirect(url_for('register_page'))

        if User.query.filter_by(email=data['email']).first():
            flash("該電子郵件已被註冊！", "danger")
            return redirect(url_for('register_page'))

        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        flash("註冊成功！", "success")
        return redirect(url_for('login_page'))

    return render_template('register.html')

# 登入
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            session['logged_in'] = True  # 標記使用者已登入
            session['user_id'] = user.id  # 存入使用者 ID
            session['is_admin'] = user.is_admin  # 存入管理員標記
            flash("登入成功！", "success")
            return redirect(url_for('index'))
        flash("無效的電子郵件或密碼！", "danger")
        return redirect(url_for('login_page'))
    return render_template('login.html')

# 登出
@app.route('/logout')
def logout_page():
    session.pop('logged_in', None)  # 清除登入狀態
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash("您已成功登出！", "info")
    return redirect(url_for('index'))  # 返回首頁

# 忘記密碼
@app.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot_password.html')

# 重設密碼
@app.route('/reset-password/<token>')
def reset_password_page(token):
    return render_template('reset_password.html', token=token)

# 個人資料
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

# 編輯個人資料
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

# 管理員使用者頁面
@app.route('/admin/user/<int:user_id>')
def admin_user_page(user_id):
    user = db.session.get(User, user_id)  # 使用 Session.get()
    if not user:
        flash("使用者不存在！", "danger")
        return redirect(url_for('admin_page'))
    return render_template('admin_user.html', user=user)

# 管理員刪除使用者
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

# 管理員更新使用者
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

# 管理員更新使用者權限
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

    if User.query.filter_by(email=email).first():
        print("該電子郵件已被註冊！請使用其他電子郵件。")
        return

    admin = User(username=username, email=email, is_admin=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print("管理者帳號已建立！")

# 初始化資料庫命令
@app.cli.command('init-db')
def init_db():
    with app.app_context():
        db.create_all()
    print("資料庫已初始化！")

# 食譜詳情
@app.route('/recipe/<int:recipe_id>')
def recipe_page(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', recipe=recipe)

# 新增食譜，需登入
@app.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe_page():
    if 'logged_in' not in session:
        flash("請先登入！", "danger")
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        data = request.form
        user_id = session['user_id']
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        recipe = Recipe(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            ingredients=data['ingredients'],
            steps=data['steps'],
            image=filename,
            user_id=user_id
        )
        db.session.add(recipe)
        db.session.commit()
        flash("食譜新增成功！", "success")
        return redirect(url_for('index'))
    return render_template('create_recipe.html')

# 編輯食譜，需登入，作者才能編輯
@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe_page(recipe_id):
    if 'logged_in' not in session:
        flash("請先登入！", "danger")
        return redirect(url_for('login_page'))

    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != session['user_id']:
        flash("無權限編輯此食譜", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        data = request.form
        recipe.title = data['title']
        recipe.description = data['description']
        recipe.category = data['category']
        recipe.ingredients = data['ingredients']
        recipe.steps = data['steps']
        db.session.commit()
        flash("食譜更新成功！", "success")
        return redirect(url_for('recipe_page', recipe_id=recipe.id))

    return render_template('edit_recipe.html', recipe=recipe)

# 刪除食譜，需登入，作者才能刪除
@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe_page(recipe_id):
    if 'logged_in' not in session:
        flash("請先登入！", "danger")
        return redirect(url_for('login_page'))

    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != session['user_id']:
        flash("無權限刪除此食譜", "danger")
        return redirect(url_for('index'))

    db.session.delete(recipe)
    db.session.commit()
    flash("食譜已刪除！", "success")
    return redirect(url_for('index'))

# 啟動應用
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 建立資料庫
    app.run(debug=True)  # 啟動開發伺服器