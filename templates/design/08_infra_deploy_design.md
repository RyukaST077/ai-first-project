---
title: インフラ・デプロイ設計書（テンプレート）
project: "<プロジェクト名>"
version: "v0.1"
last_updated: "YYYY-MM-DD"
---

# 1. インフラ構成図
```mermaid
graph TD
    User --> CloudFront
    CloudFront --> S3[S3 (Frontend)]
    User --> ALB
    ALB --> ECS[ECS/Fargate (Backend)]
    ECS --> RDS[Aurora RDS (MySQL)]
    ECS --> Redis[ElastiCache]
```

# 2. リソース定義
## 2.1 コンピューティング
- **Frontend**: AWS S3 + CloudFront (SPA Hosting)
- **Backend**: AWS Fargate (Docker)
  - CPU: 2vCPU
  - Memory: 4GB
  - AutoScaling: 2 ~ 10 tasks

## 2.2 ネットワーク
- VPC: 10.0.0.0/16
- Subnets: Public (ALB, NAT), Private (ECS), Isolated (RDS)

# 3. デプロイパイプライン (CI/CD)
## 3.1 ワークフロー
1. GitHubへPush
2. GitHub Actions起動
   - Lint / Test
   - Build (Docker Image)
3. ECRへPush
4. ECSサービスの強制更新 (Rolling Update)

## 3.2 環境分離
| 環境 | Branch | Trigger | URL |
|---|---|---|---|
| Dev | develop | Push | dev.example.com |
| Stg | main | Push | stg.example.com |
| Prod | tag (v*) | Manual Approval | example.com |

# 4. 環境変数管理
- 機密情報（DBパスワード等）は AWS Secrets Manager / Parameter Store で管理。
- アプリケーション起動時に環境変数として注入する。

| Key | Description | Dev Value | Prod Value |
|---|---|---|---|
| DB_HOST | DBホスト名 | dev-db... | prod-db... |
| API_KEY | 外部APIキー | test-key | (secret) |
