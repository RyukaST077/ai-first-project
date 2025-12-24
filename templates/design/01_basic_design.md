---
title: 基本設計書（テンプレート）
project: "<プロジェクト名>"
version: "v0.1"
last_updated: "YYYY-MM-DD"
---

# 1. はじめに
## 1.1 文書管理
| 版数 | 日付 | 改訂内容 | 作成者 |
|---|---|---|---|
| v0.1 | YYYY-MM-DD | 初版作成 | Name |

## 1.2 参考資料
- [要件定義書](link)
- [UIデザイン案](link)

# 2. 機能一覧 (Functional Requirements)
> システムが提供する機能を列挙する。

| ID | 機能名 | 概要 | 優先度 | ロール |
|---|---|---|---|---|
| F-01 | ユーザー登録 | メール/パスワードでの新規登録 | 高 | Guest |
| F-02 | ログイン | 登録済みユーザーの認証 | 高 | Guest |
| F-03 | マイページ | 自身の情報閲覧・編集 | 中 | User |

# 3. 業務フロー (Business Flow)
> 主要なユースケースの流れを記述する。

```mermaid
sequenceDiagram
    actor User
    participant App
    participant Server
    
    User->>App: 登録ボタン押下
    App->>Server: 登録リクエスト
    Server-->>App: メール送信完了
    App-->>User: 確認メール案内表示
```

# 4. 画面遷移図 (Screen Transition)
```mermaid
graph TD
    S01[ログイン] --> S02[ホーム]
    S02 --> S03[設定]
    S02 --> S04[詳細]
```

# 5. 共通仕様・非機能要件概略
- **対応ブラウザ**: Chrome, Safari (Latest)
- **多言語対応**: 日本語のみ (v1)
- **ログ**: 操作ログを3ヶ月保存
