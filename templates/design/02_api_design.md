---
title: API設計書（テンプレート）
endpoint: "GET /v1/users/{id}"
version: "v0.1"
last_updated: "YYYY-MM-DD"
---

# 1. 概要
ユーザーIDを指定して、ユーザーの詳細情報を取得する。

# 2. アクセス制御・認証
- **認証**: 必須 (Bearer Token)
- **認可**: 本人のみ、または管理者権限が必要

# 3. リクエスト
## 3.1 ヘッダー
| Key | Value | Required | 備考 |
|---|---|---|---|
| Authorization | Bearer <token> | Yes | - |

## 3.2 パスパラメータ
| Name | Type | Description | Example |
|---|---|---|---|
| id | string | ユーザーID (UUID) | 12345 |

## 3.3 クエリパラメータ
| Name | Type | Required | Description | Example |
|---|---|---|---|---|
| fields | string | No | 取得フィールド指定 | email,name |

## 3.4 リクエストボディ
- なし

# 4. レスポンス
## 4.1 成功時 (200 OK)
```json
{
  "id": "12345",
  "name": "Taro Yamada",
  "email": "taro@example.com",
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z"
}
```

## 4.2 エラー時
| Code | Error Type | Message | Description |
|---|---|---|---|
| 400 | Bad Request | Invalid ID format | IDの形式不正 |
| 401 | Unauthorized | Token required | トークンなし/期限切れ |
| 403 | Forbidden | Access denied | 他人のデータへのアクセス |
| 404 | Not Found | User not found | 対象ユーザーが存在しない |

# 5. 備考
- キャッシュ制御: `Cache-Control: private, max-age=60`
