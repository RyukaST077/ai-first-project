---
name: save-knowledge
description: バグ調査・障害対応・設定変更・運用トラブルの「症状 → 切り分け → 対処 → 結果」を、会話履歴と現在のリポジトリ状態から抽出し、プロジェクトルート直下の `knowledge/YYYY/YYYY-MM-DD-<slug>.md` に YAML frontmatter 付き Markdown で 1 件保存する Skill。ユーザが「このトラブルをナレッジ化して」「今の解決内容を残して」「/save-knowledge」などと言ったときに起動する。日報・雑談ログ・単なる気付き・会議メモには使わない。既存ナレッジの更新ではなく新規作成専用。
---

# save-knowledge

Store issues and responses that occurred within the project as a **single reusable knowledge entry** in `knowledge/`.

## Procedure

1. **Collect Context**
   - Extract symptoms, investigation steps, actions taken, and results from this session’s conversation history
   - Run `git status`, `git diff --stat`, and `git log -n 5 --oneline` to identify related modified files
   - If necessary, use Read to check relevant sections of changed files or error logs
   - Use the repository root directory name as the default project name

2. **Create Entry**
   - Read `.claude/skills/save-knowledge/reference/knowledge_entry_template.md` and construct the entry following the defined frontmatter schema and Markdown template
   - File name format: `knowledge/<YYYY>/<YYYY-MM-DD>-<kebab-slug>.md`
   - Slug must be lowercase English letters + hyphens. For Japanese titles, translate key points into English or use short romaji
   - Create `knowledge/<YYYY>/` if it does not exist
   - Do not write obvious secrets (API keys, passwords, personal names) as-is; replace them with `<REDACTED>`

3. **Self-Validation of Required Fields**
   - Verify that all **required keys** in “1. Frontmatter Schema” from the template read in step 2 are filled
   - If even one required field is missing, or contains `TBD`, an empty string, or a placeholder, **do not save**
   - Ask the user only once for the missing keys
   - Reflect the response, re-validate, and proceed only when all fields are filled

4. **Save**
   - If a file with the same name already exists, do not overwrite it; propose an alternative slug to the user and get confirmation
   - Write the file to the specified path
   - Return the absolute save path and a summary of the frontmatter (title / tags / generalizable / confidentiality), each on its own line