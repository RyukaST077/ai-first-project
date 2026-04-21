---
name: review
description: `main...HEAD` の差分だけを対象にコードレビューし、`docs/reviews/<review-title>.md` を作成するときに使う。`templates/review_list.md` または bundled reference の観点に従い、差分が導入したアクション可能な問題だけを重大度順に報告する。

---

# Review

Use this skill to review only the diff against `main` and write the result to `docs/reviews/<review-title>.md`.

## Required Inputs

- review target: current branch diff against `main...HEAD`
- checklist source: `templates/review_list.md`

## Bundled References

- Read `references/review_report_template.md` first and follow the output structure.
- If the repository has `templates/review_list.md`, treat it as the project-local source of truth.
- If `templates/review_list.md` is missing, fall back to `references/review_list.md`.

## Safety Rules

- Review only. Do not commit, push, rebase, reset, clean, or otherwise mutate Git history.
- Do not run destructive commands such as `rm -rf`, `git reset --hard`, `git clean -fd`, or force push.
- Do not install dependencies or access external networks.
- `git fetch` is allowed only when the environment clearly permits updating `origin/main`; if that is unclear, skip it and record the constraint.
- Redact secrets or personal data as `[REDACTED]`.
- Keep recommendations minimal and actionable. Do not propose broad rewrites or unrelated refactors.
- If evidence is insufficient, do not overclaim. Put the uncertainty in `Questions`.

## Workflow

1. Confirm repository state with read-only Git commands:
   - `git rev-parse --show-toplevel`
   - `git status --porcelain=v1`
   - `git branch --show-current`
   - `git log -1 --oneline`
2. Load the checklist source.
   - Read `templates/review_list.md` when present.
   - Otherwise read `references/review_list.md`.
   - Convert headings and bullets into an internal checklist.
   - Assign stable IDs such as `RL-001`, `RL-002`, and keep the section heading as `category`.
   - If the checklist has no explicit priority labels, infer priority using `security > correctness > performance > maintainability` and state that the priority is inferred.
3. Resolve the base ref in this order:
   - `origin/main` if `refs/remotes/origin/main` exists
   - otherwise local `main` if `refs/heads/main` exists
   - otherwise stop short of final judgment and record a question that `main` could not be found
4. Generate the diff for `${BASE_REF}...HEAD`.
   - Collect `git diff --name-status`, `git diff --stat`, and unified diff output with line numbers.
   - Focus on changed files only.
5. Inspect changed files in risk order.
   - Prioritize auth/authz, input validation, persistence, crypto/signing, secrets/logging, external I/O, billing, and config.
   - Read only the relevant hunks and surrounding code.
6. Run only already-defined project checks.
   - Inspect `package.json`, `pyproject.toml`, or equivalent config files first.
   - Run only the lint, test, and typecheck commands that are already defined.
   - Do not add dependencies or invent new commands.
   - Summarize failures briefly and incorporate them into the review.
7. Apply the checklist to the diff.
   - Report only issues introduced by the diff.
   - Ignore pre-existing issues unless the diff makes them worse.
   - Order findings by severity: `critical`, `high`, `medium`.
8. Write the review to `docs/reviews/<review-title>.md` using the bundled report template.

## Issue Requirements

Each issue must include all of the following:

- checklist ID such as `RL-xxx`
- category and checklist item
- precise location in `file:line-range` form when the diff provides enough evidence
- evidence describing what in the diff is wrong and why
- impact describing the likely consequence
- recommendation with the smallest concrete fix
- validation describing the test or manual check needed
- confidence as a float from `0.0` to `1.0`

## Writing Rules

- Report actionable problems first. Keep summary sections brief.
- Do not pad the review with praise or generic commentary.
- Use `Questions` for assumptions, missing context, and uncertain behavior.
- Use `Constraints` for environmental limits such as missing `origin/main`, skipped fetch, or tests that could not run.
- If no actionable issues are found, say so explicitly and still fill `Constraints`, `Base`, `Checklist`, `Summary`, and `Verdict`.

## Output

- Primary output: `docs/reviews/<review-title>.md`
- Required structure: `references/review_report_template.md`
- Expected outcome: a diff-focused review document grounded in the checklist and supported by concrete evidence
