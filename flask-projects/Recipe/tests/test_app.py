import pytest
from flask import url_for
from app import app, db
from models import User, Recipe

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SERVER_NAME'] = 'localhost'  # 配置 SERVER_NAME
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index(client):
    """測試首頁(食譜列表)"""
    response = client.get(url_for('index'))
    assert response.status_code == 200
    assert "歡迎來到 Flask App".encode('utf-8') in response.data

def test_register(client):
    """測試註冊"""
    response = client.post(url_for('api.register_page'), data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "註冊成功".encode('utf-8') in response.data

def test_login(client):
    """測試登入"""
    # 先註冊一個使用者
    client.post(url_for('api.register_page'), data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # 登入該使用者
    response = client.post(url_for('api.login_page'), data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "登入成功".encode('utf-8') in response.data

def test_profile(client):
    """測試查看個人資料"""
    # 先註冊並登入一個使用者
    client.post(url_for('api.register_page'), data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    client.post(url_for('api.login_page'), data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # 查看個人資料
    response = client.get(url_for('profile_page'))
    assert response.status_code == 200
    assert "個人資料".encode('utf-8') in response.data

def test_admin_page(client):
    """測試管理員頁面"""
    # 先註冊並登入一個管理員
    client.post(url_for('api.register_page'), data={
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'password'
    }, follow_redirects=True)
    admin = User.query.filter_by(email='admin@example.com').first()
    admin.is_admin = True
    db.session.commit()
    client.post(url_for('api.login_page'), data={
        'email': 'admin@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # 查看管理員頁面
    response = client.get(url_for('admin_page'))
    assert response.status_code == 200
    assert "管理員頁面".encode('utf-8') in response.data

def test_create_recipe(client):
    """測試新增食譜"""
    # 先註冊並登入一個使用者
    client.post(url_for('api.register_page'), data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    client.post(url_for('api.login_page'), data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # 新增食譜
    response = client.post(url_for('api.create_recipe'), json={
        'title': 'Test Recipe',
        'description': 'This is a test recipe.'
    }, follow_redirects=True)
    assert response.status_code == 201
    assert "Test Recipe".encode('utf-8') in response.data

def test_get_recipes(client):
    """測試獲取所有食譜"""
    # 先註冊並登入一個使用者
    client.post(url_for('api.register_page'), data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    client.post(url_for('api.login_page'), data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # 新增食譜
    client.post(url_for('api.create_recipe'), json={
        'title': 'Test Recipe',
        'description': 'This is a test recipe.'
    }, follow_redirects=True)
    
    # 獲取所有食譜
    response = client.get(url_for('api.get_recipes'))
    assert response.status_code == 200
    assert "Test Recipe".encode('utf-8') in response.data

def test_get_recipe(client):
    """測試獲取單個食譜詳情"""
    # 先註冊並登入一個使用者
    client.post(url_for('api.register_page'), data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    client.post(url_for('api.login_page'), data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # 新增食譜
    client.post(url_for('api.create_recipe'), json={
        'title': 'Test Recipe',
        'description': 'This is a test recipe.'
    }, follow_redirects=True)
    
    # 獲取單個食譜詳情
    recipe = Recipe.query.first()
    response = client.get(url_for('api.get_recipe', recipe_id=recipe.id))
    assert response.status_code == 200
    assert "Test Recipe".encode('utf-8') in response.data

def test_update_recipe(client):
    """測試編輯食譜"""
    # 先註冊並登入一個使用者
    client.post(url_for('api.register_page'), data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    client.post(url_for('api.login_page'), data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # 新增食譜
    client.post(url_for('api.create_recipe'), json={
        'title': 'Test Recipe',
        'description': 'This is a test recipe.'
    }, follow_redirects=True)
    
    # 編輯食譜
    recipe = Recipe.query.first()
    response = client.put(url_for('api.update_recipe', recipe_id=recipe.id), json={
        'title': 'Updated Recipe',
        'description': 'This is an updated test recipe.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Updated Recipe".encode('utf-8') in response.data

def test_delete_recipe(client):
    """測試刪除食譜"""
    # 先註冊並登入一個使用者
    client.post(url_for('api.register_page'), data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    client.post(url_for('api.login_page'), data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # 新增食譜
    client.post(url_for('api.create_recipe'), json={
        'title': 'Test Recipe',
        'description': 'This is a test recipe.'
    }, follow_redirects=True)
    
    # 刪除食譜
    recipe = Recipe.query.first()
    response = client.delete(url_for('api.delete_recipe', recipe_id=recipe.id), follow_redirects=True)
    assert response.status_code == 204
    assert Recipe.query.get(recipe.id) is None