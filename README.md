# TodoApp

## 概要

REST API について学んだことをアウトプットするために Python Flask で作成した Todo を管理できるアプリケーションです。
フロントエンドはGoogleのantigravityを使用し作成しました。

## ディレクトリ構成
```
portfolio-todoapp/
  ├── backend/    # Flask APIサーバー
  └── frontend/   # React フロントエンド
```

## 使用技術

### Backend
| Category            | Technology       | Reason for selection                                   |
| :------------------ | :--------------- | :----------------------------------------------------- |
| **Language**        | Python 3.11      |                                                        |
| **Framework**       | Flask            | マイクロサービス指向で軽量、かつ拡張性が高いため       |
| **API**             | Flask-Smorest    | OpenAPI (Swagger) 自動生成と REST 原則の強制のため     |
| **ORM**             | Flask-SQLAlchemy | 堅牢な DB 操作と SQL インジェクション対策のため        |
| **Schema**          | Marshmallow      | 入出力のシリアライズ・バリデーションを一元管理するため |
| **Package Manager** | uv               | pip と比較して圧倒的に高速で、依存関係地獄を防げるため |
| **Infrastructure**  | Docker           | 開発環境と本番環境の差異をなくすため                   |

### Frontend
- **React** (Vite)
- **Tailwind CSS**

## 起動方法

### Backend (Docker)
```bash
cd backend
docker compose up --build
```
APIサーバーが http://localhost:5000 で起動します。
Swagger UI: http://localhost:5000/swagger-ui

### Frontend (Local)
```bash
cd frontend
npm install
npm run dev
```
フロントエンド開発サーバーが http://localhost:5173 で起動します。
プロキシ設定により、`/api` へのリクエストは自動的にバックエンドに転送されます。

## 機能一覧

### ユーザー認証機能

ユーザー個人が自身の todo と tag を持つ構造にしました。

`Flask-JWT-Extended` を活用し、一般的なローカルストレージ保存よりも堅牢な認証システムを構築しました。

- Cookie ベースの認証 :

  - 認証トークン（JWT）をブラウザの `Cookie` に保存し、JavaScript からのアクセスを禁止（`HttpOnly=True`）。これにより、XSS によるトークン奪取を無効化しています。

- CSRF 保護 :
  - Cookie 認証の弱点である CSRF を防ぐため、保護機能を有効化して（`JWT_COOKIE_CSRF_PROTECT = True`）Cookie と CSRFT-TOKEN の両方の送信を必須にしました。

### Todo 機能

- Todo の追加 (Create)
- Todo の一覧表示 (Read)
- 特定の Todo の表示 (Read)
- Todo の部分更新 (Patch)
- Todo の削除 (Delete)

### タグ機能 (多対多リレーション)

- タグの作成 (Create)
- タグの一覧表示 (Read)
- 特定のタグの表示 (Read)
- タグの削除 (Delete)
- Todo へのタグ付け・解除 (Link/Unlink)

### テストコード

バックエンドのテスト:
```bash
cd backend
uv run pytest
```

