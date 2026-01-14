---
title: 権限・ロール定義書（テンプレート）
project: "<プロジェクト名>"
version: "v0.1"
last_updated: "YYYY-MM-DD"
---

# 1. ロール定義 (Roles)
システムにおける役割を定義する。

| Role ID | Role Name | 説明 |
|---|---|---|
| R-01 | Admin | システム全体の管理が可能。 |
| R-02 | Manager | 自部門のデータの閲覧・編集が可能。 |
| R-03 | User | 自身のデータのみ閲覧・編集が可能。 |
| R-04 | Guest | ログイン前の利用者。公開情報のみ閲覧可。 |

# 2. 権限定義 (Permissions)
システムで実行可能な操作（権限）を定義する。

| Perm ID | Permission Name | 説明 |
|---|---|---|
| P-01 | user.view | ユーザー情報を閲覧する。 |
| P-02 | user.edit | ユーザー情報を編集する。 |
| P-03 | item.delete | 商品を削除する。 |

# 3. 権限マトリクス (RBAC Matrix)
ロールと権限の対応表。

| Permission / Role | Admin (R-01) | Manager (R-02) | User (R-03) | Guest (R-04) |
|---|:---:|:---:|:---:|:---:|
| user.view | ○ | ○ | ○ (自身のみ) | - |
| user.edit | ○ | ○ | ○ (自身のみ) | - |
| item.view | ○ | ○ | ○ | ○ |
| item.edit | ○ | ○ | - | - |
| item.delete | ○ | - | - | - |

# 4. 実装・制御方針
- **API層**: Middlewareにて、トークン内のRoleを確認し、エンドポイントごとのRequired Permissionと照合する。
- **UI層**: 権限がないボタンは非表示、またはDisabledにする。
