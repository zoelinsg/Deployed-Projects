# Basic/models.py
# 定義資料庫模型與相關方法

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# 初始化資料庫與加密模組
db = SQLAlchemy()
bcrypt = Bcrypt()

# 使用者模型
class User(db.Model):
    """
    使用者資料庫模型
    """
    id = db.Column(db.Integer, primary_key=True)  # 主鍵 ID
    username = db.Column(db.String(150), nullable=False, unique=True)  # 使用者名稱
    email = db.Column(db.String(150), nullable=False, unique=True)  # 電子郵件
    password_hash = db.Column(db.String(200), nullable=False)  # 雜湊密碼
    is_admin = db.Column(db.Boolean, nullable=False, default=False)  # 管理員 (True/False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)  # 啟用
    phone = db.Column(db.String(20), nullable=True)  # 電話號碼
    bio = db.Column(db.String(150), nullable=True)  # 簡介
    address = db.Column(db.String(150), nullable=True)  # 地址
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # 建立時間
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())  # 更新時間

    def set_password(self, password):
        """
        設定密碼（雜湊處理）
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        驗證密碼
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        定義物件的字串表示形式
        """
        return f'<User {self.username}>'

# 食譜模型
class Recipe(db.Model):
    """
    食譜資料庫模型
    """
    id = db.Column(db.Integer, primary_key=True)  # 主鍵 ID
    title = db.Column(db.String(150), nullable=False)  # 食譜標題
    description = db.Column(db.Text, nullable=False)  # 食譜描述
    category = db.Column(db.String(50), nullable=False)  # 食譜類別
    ingredients = db.Column(db.Text, nullable=False)  # 食材
    steps = db.Column(db.Text, nullable=False)  # 步驟
    image = db.Column(db.String(150), nullable=True)  # 照片
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 使用者 ID
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # 建立時間
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())  # 更新時間

    def to_dict(self):
        """
        將食譜物件轉換為字典
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'ingredients': self.ingredients,
            'steps': self.steps,
            'image': self.image,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        """
        定義物件的字串表示形式
        """
        return f'<Recipe {self.title}>'