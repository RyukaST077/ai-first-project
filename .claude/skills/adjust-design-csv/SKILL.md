---
name: adjust-design-csv
description: 設計書変換用スキル
argument-hint: 変換したい設計書csvのすべてのパスを引数に指定
---

# Objective
I want to create a design document in Markdown format.

# Background
The target csv file was converted from Excel to csv using Python and contains a lot of unnecessary information.

# Request
Please review the target csv file, extract the necessary information, and compile it into a single Markdown file.

# Output File
`docs\design\message_design.md`

# Target csv Files
$ARGUMENTS