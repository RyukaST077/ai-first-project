---
description: 要件と既存コードベースの実装ギャップを分析する
allowed-tools: Bash, Glob, Grep, Read, Write, Edit, MultiEdit, WebSearch, WebFetch
argument-hint: <feature-name>
---

# 実装ギャップ検証

<background_information>
- **ミッション**: 要件と既存コードベースの差分を分析し、実装方針の判断材料を提供する
- **成功条件**:
  - 既存コードベースのパターンとコンポーネントを包括的に理解
  - 不足機能と統合課題を明確に特定
  - 複数の実装アプローチを比較評価
  - 設計フェーズで必要な技術調査項目を特定
</background_information>

<instructions>
## 主タスク
承認済み要件と既存コードベースを基に、機能 **$1** の実装ギャップを分析する。

## 実行手順

1. **Load Context**:
   - `{{KIRO_DIR}}/specs/$1/spec.json` を読み、言語とメタデータを確認
   - `{{KIRO_DIR}}/specs/$1/requirements.md` を読み、要件を確認
   - **steering 文脈をすべて読み込む**: `{{KIRO_DIR}}/.memory-bank/steering/` 全体（以下を含む）
     - 既定ファイル: `structure.md`, `tech.md`, `product.md`
     - モード設定に関係なく、すべてのカスタム steering
     - 完全なプロジェクト記憶と文脈を提供

2. **Read Analysis Guidelines**:
   - `{{KIRO_DIR}}/settings/rules/gap-analysis.md` を読み、包括分析フレームワークを確認

3. **Execute Gap Analysis**:
   - gap-analysis.md フレームワークに従って調査
   - Grep と Read で既存コードベースを分析
   - 必要時は WebSearch/WebFetch で外部依存を調査
   - 複数の実装アプローチ（extend/new/hybrid）を評価
   - 出力言語は spec.json 指定に従う

4. **Generate Analysis Document**:
   - gap-analysis.md の出力ガイドに沿って包括的分析を作成
   - トレードオフ付きで複数の実行可能案を提示
   - 追加調査が必要な領域を明示

## 重要な制約
- **決定より情報提供**: 最終実装判断ではなく、分析と選択肢を提示
- **複数案提示**: 可能な場合は代替案を示す
- **徹底調査**: ツールで既存コードベースを深く理解
- **ギャップ明示**: 追加調査が必要な箇所を明確に示す
</instructions>

## ツールガイダンス
- **Read first**: 分析前に全コンテキスト（spec、steering、rules）を読み込む
- **Grep extensively**: パターン、規約、統合ポイントを広く探索
- **WebSearch/WebFetch**: 必要に応じて外部依存とベストプラクティスを調査
- **Write last**: 調査完了後に分析を生成

## 出力仕様
spec.json 指定言語で以下を出力:

1. **分析サマリー**: 範囲・課題・推奨の概要（3〜5項目）
2. **文書状態**: 実施した分析アプローチを確認
3. **次ステップ**: 設計フェーズへの進め方を案内

**形式要件**:
- 可読性のため Markdown 見出しを使用
- サマリーは簡潔に（300語未満）
- 詳細分析は gap-analysis.md の出力ガイドラインに従う

## 安全性とフォールバック

### エラーシナリオ
- **要件不足**: requirements.md がなければ停止し、"Run `/kiro:spec-requirements $1` first to generate requirements" と案内
- **要件未承認**: 未承認でも警告のうえ続行（ギャップ分析は要件見直しにも有用）
- **steering 空**: プロジェクト文脈不足で分析品質へ影響し得ることを警告
- **複雑統合が不明瞭**: ブロックせず、設計フェーズでの包括調査事項として明示
- **言語未定義**: spec.json に言語がなければ英語（`en`）を既定にする

### 次フェーズ: 設計生成

**ギャップ分析完了時**:
- ギャップ分析の知見を確認
- `/kiro:spec-design $1` で技術設計文書を作成
- または `/kiro:spec-design $1 -y` で要件自動承認して進行

**補足**: ギャップ分析は任意だが、ブラウンフィールドでは設計判断に有益。
