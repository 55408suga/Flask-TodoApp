# Portfolio TodoApp

## 概要 (Overview)

REST APIs with Flask and Python in 2025 という Udemy の講座で学んだことをアウトプットするために作成した、Flask での初めてのアプリケーションです。今後様々な機能を実装予定です。

## 使用技術

| Category            | Technology       | Reason for selection                                   |
| :------------------ | :--------------- | :----------------------------------------------------- |
| **Language**        | Python 3.11      |                                                        |
| **Framework**       | Flask            | マイクロサービス指向で軽量、かつ拡張性が高いため       |
| **API**             | Flask-Smorest    | OpenAPI (Swagger) 自動生成と REST 原則の強制のため     |
| **ORM**             | Flask-SQLAlchemy | 堅牢な DB 操作と SQL インジェクション対策のため        |
| **Schema**          | Marshmallow      | 入出力のシリアライズ・バリデーションを一元管理するため |
| **Package Manager** | **uv**           | pip と比較して圧倒的に高速で、依存関係地獄を防げるため |
| **Infrastructure**  | Docker           | 開発環境と本番環境の差異をなくすため                   |

## 起動方法

### Docker を使用する場合（推奨）

以下のコマンドを実行するだけで、環境構築からサーバー起動まで完了します。

```bash
# 1. リポジトリのクローン
git clone [https://github.com/55408suga/Flask-TodoApp.git](https://github.com/55408suga/Flask-TodoApp.git)
cd Flask-TodoApp

# 2. ビルドと起動
docker compose up --build
```

## 機能一覧

- Todo の追加　 Create
- Todo の一覧表示　 Read
- 特定の Todo の表示　 Read
- Todo の更新　 Patch
- Todo の削除　 Delete

## 実装予定の機能

- タグ付け機能:多対多のリレーションシップ実装
- ユーザー認証：セキュリティ強化
- フロントエンド実装
- テストコード
