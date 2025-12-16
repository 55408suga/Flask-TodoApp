def test_user_flow_happy_path(client):
    """
    正常系シナリオ: 登録 -> ログイン -> Todo作成 -> 一覧確認 -> 削除
    """
    # 1. ユーザー登録
    res = client.post("/api/register", json={
        "username": "hero_tanaka",
        "password": "secure_password"
    })
    assert res.status_code == 201

    # 2. ログイン
    res = client.post("/api/login", json={
        "username": "hero_tanaka",
        "password": "secure_password"
    })
    assert res.status_code == 204
    
    # ★修正ポイント1: ヘッダーからクッキーを確認する
    # "Set-Cookie" ヘッダーの中に "access_token_cookie" という文字が含まれているか？
    cookies = res.headers.getlist("Set-Cookie")
    assert any("access_token_cookie" in c for c in cookies)

    # 3. Todo作成 (Cookieはclientが勝手に持っている状態)
    res = client.post("/api/todos", json={
        "name": "世界を救う",
        "is_done": False
    })
    assert res.status_code == 204

    # 4. Todo一覧取得
    res = client.get("/api/todos")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "世界を救う"


def test_data_privacy(client, auth_client):
    """
    データ分離シナリオ: AさんのTodoは、Bさんからは見えないこと
    """
    # --- Aさんの行動 ---
    # Aさんとしてログイン
    client_a = auth_client(username="user_A", password="passwordA")
    
    # AさんがTodoを作る
    client_a.post("/api/todos", json={"name": "Aの秘密タスク"})
    
    # 確認: Aさんは見える
    res = client_a.get("/api/todos")
    assert len(res.get_json()) == 1

    # --- クライアントのクッキーを削除（ログアウト扱い） ---
    # ★修正ポイント2: delete_cookieを使う
    client.delete_cookie("access_token_cookie")
    client.delete_cookie("refresh_token_cookie")
    client.delete_cookie("csrf_access_token")

    # --- Bさんの行動 ---
    # Bさんとして登録＆ログイン (同じclientを使っても、クッキーは上書きされる)
    # auth_client内部で login を呼ぶので、新しいクッキーがセットされます
    client_b = auth_client(username="user_B", password="passwordB")

    # 確認: Bさんが一覧を見ても、Aのタスクは入っていない（空っぽ）はず！
    res = client_b.get("/api/todos")
    assert res.status_code == 200
    assert len(res.get_json()) == 0  # ここが 0 ならテスト成功！


def test_create_todo_without_login(client):
    """
    セキュリティシナリオ: ログインしていないとTodoは作れない
    """
    # クッキーを確実に消しておく
    client.delete_cookie("access_token_cookie")
    
    # ログインせずに叩く
    res = client.post("/api/todos", json={"name": "不正なタスク"})
    
    # 401 (Unauthorized) が返るはず
    assert res.status_code == 401