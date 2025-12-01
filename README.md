# TodoApp

## 概要

REST APIs with Flask and Python in 2025 という Udemy の講座で学んだことをアウトプットするために作成した、Flask での Todo を管理できるアプリケーションです。今後様々な機能を実装予定です。

## 使用技術

| Category            | Technology       | Reason for selection                                   |
| :------------------ | :--------------- | :----------------------------------------------------- |
| **Language**        | Python 3.11      |                                                        |
| **Framework**       | Flask            | マイクロサービス指向で軽量、かつ拡張性が高いため       |
| **API**             | Flask-Smorest    | OpenAPI (Swagger) 自動生成と REST 原則の強制のため     |
| **ORM**             | Flask-SQLAlchemy | 堅牢な DB 操作と SQL インジェクション対策のため        |
| **Schema**          | Marshmallow      | 入出力のシリアライズ・バリデーションを一元管理するため |
| **Package Manager** | uv               | pip と比較して圧倒的に高速で、依存関係地獄を防げるため |
| **Infrastructure**  | Docker           | 開発環境と本番環境の差異をなくすため                   |

## 起動方法

### Docker を使用する場合

以下のコマンドを実行するだけで、環境構築からサーバー起動まで完了します。

```bash
# 1. リポジトリのクローン
git clone https://github.com/55408suga/Flask-TodoApp.git
cd Flask-TodoApp
```

```bash
# 2. ビルドと起動
docker compose up --build
```

### API ドキュメント (Swagger UI)

サーバー起動後、以下の URL にアクセスすると、自動生成された API 仕様書の閲覧およびブラウザ上での API テストが可能です。

**URL:** [http://localhost:5000/swagger-ui](http://localhost:5000/swagger-ui)

## 機能一覧

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

## 実装予定の機能

- ユーザー認証：セキュリティ強化
- フロントエンド実装
- テストコード
