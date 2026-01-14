---
title: アーキテクチャ設計書（テンプレート）
project: "<プロジェクト名>"
version: "v0.1"
last_updated: "YYYY-MM-DD"
---

# 1. システム全体像
## 1.1 コンテキスト図
> システムと外部システム、ユーザーの関係を示す。

```mermaid
graph LR
    User((ユーザー)) --> app[Webアプリ]
    app --> api[APIサーバー]
    api --> db[(Database)]
    api --> ext[外部決済API]
```

# 2. 技術スタック
| カテゴリ | 技術要素 | バージョン | 選定理由 |
|---|---|---|---|
| フロントエンド | Next.js / React | | SEO, パフォーマンス |
| バックエンド | Go / Node.js | | 型安全性, 開発速度 |
| データベース | PostgreSQL | | 信頼性 |
| インフラ | AWS / GCP | | スケーラビリティ |

# 3. アプリケーションアーキテクチャ
## 3.1 ディレクトリ構成
```
/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── hooks/
├── backend/
│   ├── cmd/
│   ├── internal/
│   │   ├── handler/
│   │   ├── usecase/
│   │   └── repository/
└── infra/
```

# 4. データフロー
> 主要な処理（検索、更新など）のデータフローを記述。

1. クライアントがAPIリクエスト送信
2. Handlerがリクエスト検証
3. Usecaseがビジネスロジック実行
4. RepositoryがDBアクセス
5. ...