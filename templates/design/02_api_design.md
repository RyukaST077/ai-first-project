---
title: API設計書（テンプレート）
endpoint: "GET /v1/users/{id}"
version: "v0.1"
last_updated: "YYYY-MM-DD"
---

# 1. 概要
ユーザーIDを指定して、ユーザーの詳細情報を取得する。

## 1.1 OpenAPI / Swagger
- **OpenAPI定義ファイル**: `openapi/users.yaml`
- **Swagger UI**: `https://api.example.com/docs`
- **自動生成**: OpenAPI定義から型定義・クライアントコードを自動生成
- **リンター**: Spectral等でAPI設計ルールを検証

# 2. APIバージョニング戦略
| 項目 | 内容 |
|---|---|
| **バージョン管理方式** | URLパス方式 (例: `/v1/`, `/v2/`) |
| **現在のバージョン** | v1 |
| **サポートポリシー** | 新バージョンリリース後、旧バージョンは6ヶ月サポート |
| **非推奨の通知** | レスポンスヘッダー `Deprecation: true`、`Sunset: <日付>` で通知 |
| **破壊的変更** | メジャーバージョンアップ時のみ許可 |

# 3. アクセス制御・認証
- **認証**: 必須 (Bearer Token)
- **認可**: 本人のみ、または管理者権限が必要

## 3.1 レート制限 (Rate Limiting)
| ユーザー種別 | リクエスト上限 | 時間枠 | 超過時の挙動 |
|---|---|---|---|
| 未認証 | 100 req | 1時間 | HTTP 429 + Retry-After ヘッダー |
| 一般ユーザー | 1,000 req | 1時間 | HTTP 429 + Retry-After ヘッダー |
| プレミアム | 10,000 req | 1時間 | HTTP 429 + Retry-After ヘッダー |

**レスポンスヘッダー**:
- `X-RateLimit-Limit`: 上限値
- `X-RateLimit-Remaining`: 残り回数
- `X-RateLimit-Reset`: リセット時刻 (Unix timestamp)

# 4. リクエスト
## 4.1 ヘッダー
| Key | Value | Required | 備考 |
|---|---|---|---|
| Authorization | Bearer <token> | Yes | - |
| Content-Type | application/json | Yes (POST/PUT) | - |
| Accept | application/json | No | デフォルトはJSON |
| Accept-Language | ja, en | No | 多言語対応時に使用 |

## 4.2 パスパラメータ
| Name | Type | Description | Example |
|---|---|---|---|
| id | string | ユーザーID (UUID) | 12345 |

## 4.3 クエリパラメータ
| Name | Type | Required | Description | Example |
|---|---|---|---|---|
| fields | string | No | 取得フィールド指定 (カンマ区切り) | email,name |
| include | string | No | 関連リソースを含める | profile,orders |

### ページネーション（一覧系APIで使用）
| Name | Type | Required | Description | Example |
|---|---|---|---|---|
| page | integer | No | ページ番号 (1始まり) | 1 |
| per_page | integer | No | 1ページあたりの件数 (デフォルト: 20, 最大: 100) | 20 |
| cursor | string | No | カーソルベースページネーション用 | eyJpZCI6MTIzfQ== |

### ソート・フィルタリング（一覧系APIで使用）
| Name | Type | Required | Description | Example |
|---|---|---|---|---|
| sort | string | No | ソート項目 (+昇順, -降順) | -created_at,+name |
| filter[status] | string | No | ステータスでフィルタ | active |

## 4.4 リクエストボディ
- なし（GET リクエストのため）

**POST/PUT リクエストの例**:
```json
{
  "name": "Taro Yamada",
  "email": "taro@example.com",
  "profile": {
    "bio": "Software Engineer",
    "location": "Tokyo"
  }
}
```

# 5. レスポンス
## 5.1 成功時 (200 OK)
### レスポンスヘッダー
| Header | Value | 説明 |
|---|---|---|
| Content-Type | application/json | - |
| X-Request-ID | uuid | リクエスト追跡用ID |
| X-RateLimit-* | (数値) | レート制限情報 |

### レスポンスボディ
**単一リソースの場合**:
```json
{
  "id": "12345",
  "name": "Taro Yamada",
  "email": "taro@example.com",
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

**一覧リソースの場合（ページネーション付き）**:
```json
{
  "data": [
    {
      "id": "12345",
      "name": "Taro Yamada",
      "email": "taro@example.com"
    }
  ],
  "pagination": {
    "current_page": 1,
    "per_page": 20,
    "total_pages": 5,
    "total_count": 100,
    "next_cursor": "eyJpZCI6MTIzfQ=="
  },
  "links": {
    "self": "/v1/users?page=1",
    "next": "/v1/users?page=2",
    "prev": null,
    "first": "/v1/users?page=1",
    "last": "/v1/users?page=5"
  }
}
```

## 5.2 エラー時
### エラーコード一覧
| Code | Error Type | Message | Description |
|---|---|---|---|
| 400 | Bad Request | Invalid ID format | IDの形式不正 |
| 401 | Unauthorized | Token required | トークンなし/期限切れ |
| 403 | Forbidden | Access denied | 他人のデータへのアクセス |
| 404 | Not Found | User not found | 対象ユーザーが存在しない |
| 422 | Unprocessable Entity | Validation failed | バリデーションエラー |
| 429 | Too Many Requests | Rate limit exceeded | レート制限超過 |
| 500 | Internal Server Error | Internal error | サーバー内部エラー |
| 503 | Service Unavailable | Service temporarily unavailable | メンテナンス中 |

### エラーレスポンス形式
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力値が不正です",
    "details": [
      {
        "field": "email",
        "message": "メールアドレスの形式が正しくありません"
      }
    ],
    "request_id": "req_abc123",
    "timestamp": "2024-01-01T10:00:00Z"
  }
}
```

# 6. 備考
## 6.1 キャッシュ制御
- `Cache-Control: private, max-age=60` （個人データは60秒キャッシュ）
- `Cache-Control: public, max-age=3600` （公開データは1時間キャッシュ）
- `ETag` ヘッダーによる条件付きリクエスト対応

## 6.2 セキュリティ
- CORS: 許可オリジンは環境変数で管理
- CSRF対策: SameSite Cookie + カスタムヘッダー検証
- SQL Injection / XSS 対策: 入力値の検証・エスケープ

## 6.3 パフォーマンス
- レスポンス圧縮: gzip/brotli 対応
- フィールド選択: `?fields=id,name` で不要な項目を除外可能
- バッチリクエスト: 将来的に `/batch` エンドポイントで複数リクエストをまとめて処理

## 6.4 監視・デバッグ
- `X-Request-ID` ヘッダーでリクエストを追跡
- ログレベル: INFO (成功), WARN (4xx), ERROR (5xx)
- メトリクス: レスポンスタイム、エラー率、レート制限ヒット数
