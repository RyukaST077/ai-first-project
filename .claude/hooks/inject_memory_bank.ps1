[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$projectDir = $env:CLAUDE_PROJECT_DIR
if (-not $projectDir) { exit 0 }

$memoryDir = Join-Path $projectDir 'MemoryBank'
$targets = @(
    'activeContext.md',
    'decisionLog.md',
    'openQuestions.md'
)

$parts = @()

foreach ($name in $targets) {
    $path = Join-Path $memoryDir $name
    if (Test-Path $path) {
        $text = Get-Content -Path $path -Raw -Encoding UTF8
        if ($text.Length -gt 4000) {
            $text = $text.Substring(0, 4000) + "`n`n... (truncated)"
        }
        $parts += "# $name`n$text`n"
    }
}

if ($parts.Count -gt 0) {
    "Reinjected context after compaction. Prioritize the following MemoryBank contents:`n`n$($parts -join "`n")"
}