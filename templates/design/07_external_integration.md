---
title: 外部システム連携仕様書（テンプレート）
target_system: "<連携先システム名>"
version: "v0.1"
last_updated: "YYYY-MM-DD"
---

# 1. 連携概要
## 1.1 目的
- 決済処理を行うため、Stripe APIを利用する。
- ユーザーへのメール配信のため、SendGridを利用する。

## 1.2 接続方式
- **Protocol**: HTTPS (REST API)
- **Format**: JSON
- **Auth**: Bearer Token (API Key)

# 2. API仕様 (利用するエンドポイント)
## 2.1 決済作成 (POST /v1/charges)
- **用途**: 注文確定時に実行
- **Input**: amount, currency, source
- **Output**: charge_id, status

## 2.2 顧客作成 (POST /v1/customers)
- **用途**: 会員登録時に実行
- ...

# 3. エラーハンドリング・障害対策
## 3.1 タイムアウト設定
- Connection Timeout: 5s
- Read Timeout: 10s

## 3.2 リトライポリシー
- **対象エラー**: Network Error, 500, 502, 503, 504
- **非対象エラー**: 400, 401, 403, 404
- **回数**: 3回 (Exponential Backoff)

## 3.3 フォールバック
- 決済APIがダウンしている場合、「現在メンテナンス中です」を表示し、注文を受け付けない。

# 4. テスト環境
- **Sandbox**: 利用可能 (テスト用APIキーを使用)
- **テストカード**:
  - 成功: 4242...
  - 失敗: 4000...
