import os
from flask import Blueprint, request, jsonify, render_template, flash, redirect, session, url_for
from werkzeug.utils import secure_filename
from models import Recipe, db, User
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail

# 初始化 Blueprint 與 Token 生成器
api = Blueprint('api', __name__)  # 定義 Blueprint
s = URLSafeTimedSerializer('your_secret_key')  # 用於生成與解析重設密碼的 token
mail = Mail()  # 初始化 Flask-Mail

# 設定上傳文件夾和允許的文件類型
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 檢查文件類型是否允許
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 首頁 API(歡迎信息)，食譜列表
@api.route('/', methods=['GET'])
def index():
    """
    返回基本歡迎信息的 API
    """
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

# 註冊 API
@api.route('/register', methods=['GET', 'POST'])
def register_page():
    """
    註冊頁面與處理邏輯
    """
    if request.method == 'POST':
        data = request.form  # 接收表單資料
        if not all(k in data for k in ('username', 'email', 'password')):
            flash("所有欄位為必填！", "danger")
            return redirect(url_for('api.register_page'))

        if User.query.filter_by(email=data['email']).first():
            flash("該電子郵件已被註冊！", "danger")
            return redirect(url_for('api.register_page'))

        # 建立新使用者
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        flash("註冊成功！", "success")
        return redirect(url_for('api.login_page'))

    return render_template('register.html')

# 登入 API
@api.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    處理登入邏輯
    """
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
        return redirect(url_for('api.login_page'))
    return render_template('login.html')

# 登出 API
@api.route('/logout', methods=['GET'])
def logout():
    """
    處理登出邏輯
    """
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash("已成功登出！", "info")
    return redirect(url_for('index'))

# 個人資料 API
@api.route('/profile', methods=['GET', 'POST'])
def get_profile():
    """
    查看與修改個人資料
    """
    if 'logged_in' not in session:
        flash("請先登入！", "danger")
        return redirect(url_for('api.login_page'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "使用者不存在"}), 404

    if request.method == 'POST':
        data = request.form
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.bio = data.get('bio', user.bio)
        user.address = data.get('address', user.address)
        db.session.commit()
        flash("個人資料已更新", "success")

    return render_template('profile.html', user=user)

# 忘記密碼 API
@api.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    處理忘記密碼
    """
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='password-reset')
            reset_url = url_for('api.reset_password', token=token, _external=True)
            msg = Message(
                "重設密碼請求",
                sender="noreply@example.com",
                recipients=[email]
            )
            msg.body = f"請點擊以下連結重設密碼：\n{reset_url}"
            mail.send(msg)
            flash("密碼重設連結已發送！", "info")
        else:
            flash("找不到該電子郵件！", "danger")
        return redirect(url_for('api.forgot_password'))
    return render_template('forgot_password.html')

# 重設密碼 API
@api.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    處理重設密碼
    """
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)  # 驗證 token 有效性（1 小時）
    except Exception:
        flash("無效或已過期的連結！", "danger")
        return redirect(url_for('api.forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            db.session.commit()
            flash("密碼重設成功！", "success")
            return redirect(url_for('api.login_page'))
        flash("使用者不存在！", "danger")

    return render_template('reset_password.html', token=token)

# 管理者 API
@api.route('/admin', methods=['GET'])
def admin_page():
    """
    管理者頁面
    """
    if 'logged_in' not in session or not session.get('is_admin'):
        flash("權限不足！", "danger")
        return redirect(url_for('api.login_page'))

    users = User.query.all()
    return render_template('admin.html', users=users)

# 食譜列表 API(首頁)
@api.route('/recipes', methods=['GET'])
def get_recipes():
    """
    獲取所有食譜
    """
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes]), 200

# 食譜詳情 API
@api.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """
    獲取單個食譜詳情
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict()), 200

# 新增食譜，需登入
@api.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe_page():
    """
    新增食譜
    """
    if 'logged_in' not in session:
        flash("請先登入！", "danger")
        return redirect(url_for('api.login_page'))

    if request.method == 'POST':
        data = request.form
        user_id = session['user_id']
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
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

# 編輯食譜 API
@api.route('/recipe/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    """
    編輯食譜
    """
    if 'logged_in' not in session:
        flash("請先登入！", "danger")
        return redirect(url_for('api.login_page'))

    data = request.get_json()
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != session['user_id']:
        return jsonify({"error": "無權限編輯此食譜"}), 403

    recipe.title = data['title']
    recipe.description = data['description']
    recipe.category = data['category']
    recipe.ingredients = data['ingredients']
    recipe.steps = data['steps']
    db.session.commit()
    return jsonify(recipe.to_dict()), 200

# 刪除食譜 API
@api.route('/recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """
    刪除食譜
    """
    if 'logged_in' not in session:
        flash("請先登入！", "danger")
        return redirect(url_for('api.login_page'))

    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != session['user_id']:
        return jsonify({"error": "無權限刪除此食譜"}), 403

    db.session.delete(recipe)
    db.session.commit()
    return '', 204

# 初始化 Flask-Mail
def init_app(app):
    mail.init_app(app)
    app.register_blueprint(api)