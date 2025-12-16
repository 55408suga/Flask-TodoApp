import pytest
from app import create_app
from db import db

# テスト用のアプリ設定
@pytest.fixture
def app():
    # テスト用の設定（メモリ上のDBを使う、CSRFチェックを無効化するなど）
    app = create_app("sqlite:///:memory:")
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_COOKIE_CSRF_PROTECT": False, # テストを簡単にするためOFF
    })

    # テスト開始時にDBを作る
    with app.app_context():
        db.create_all()
        yield app
        # テスト終了時にDBを消す
        db.session.remove()
        db.drop_all()

# テスト用のクライアント（ブラウザの代わり）
@pytest.fixture
def client(app):
    return app.test_client()

# ユーザー作成＆ログイン済みのクライアントを返す便利機能
@pytest.fixture
def auth_client(client):
    def _auth_client(username="testuser", password="password"):
        # 1. 登録
        client.post("/api/register", json={"username": username, "password": password})
        # 2. ログイン (これでCookieがclientに保存される)
        client.post("/api/login", json={"username": username, "password": password})
        return client
    return _auth_client