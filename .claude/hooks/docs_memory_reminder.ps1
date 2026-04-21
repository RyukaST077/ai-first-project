[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Read-HookInput {
    try {
        $raw = [Console]::In.ReadToEnd()
        if ([string]::IsNullOrWhiteSpace($raw)) { return $null }
        return $raw | ConvertFrom-Json -Depth 100
    } catch {
        return $null
    }
}

function Normalize-ForwardSlashPath([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path)) { return "" }
    try {
        $full = [System.IO.Path]::GetFullPath($Path)
    } catch {
        $full = $Path
    }
    return ($full -replace '\\', '/').TrimEnd('/')
}

function Get-ProjectRelativePath([string]$FilePath, [string]$ProjectDir) {
    $file = Normalize-ForwardSlashPath $FilePath
    $proj = Normalize-ForwardSlashPath $ProjectDir

    if ($proj -and $file.StartsWith($proj + '/', [System.StringComparison]::OrdinalIgnoreCase)) {
        return $file.Substring($proj.Length + 1)
    }

    return $file
}

function StartsWithAny([string]$Value, [string[]]$Prefixes) {
    foreach ($prefix in $Prefixes) {
        if ($Value.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }
    return $false
}

$data = Read-HookInput
if (-not $data) { exit 0 }

$filePath = $data.tool_input.file_path
if (-not $filePath) { $filePath = $data.tool_response.filePath }
if (-not $filePath) { $filePath = $data.tool_response.file_path }
if (-not $filePath) { exit 0 }

$relPath = Get-ProjectRelativePath $filePath $env:CLAUDE_PROJECT_DIR

$excludedPrefixes = @(
    'Docs/',
    'docs/',
    'MemoryBank/',
    'memory-bank/',
    '.claude/'
)

if (StartsWithAny $relPath $excludedPrefixes) {
    exit 0
}

$targetPrefixes = @(
    'src/',
    'app/',
    'packages/',
    'api/',
    'db/',
    'schema/',
    'backend/',
    'frontend/'
)

$targetSuffixes = @(
    '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
    '.py', '.go', '.java', '.rb', '.php',
    '.sql', '.yaml', '.yml', '.json',
    '.cs', '.cpp', '.c', '.h'
)

$isTarget = $false
foreach ($prefix in $targetPrefixes) {
    if ($relPath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        $isTarget = $true
        break
    }
}
if (-not $isTarget) {
    foreach ($suffix in $targetSuffixes) {
        if ($relPath.EndsWith($suffix, [System.StringComparison]::OrdinalIgnoreCase)) {
            $isTarget = $true
            break
        }
    }
}

if (-not $isTarget) { exit 0 }

$message = "The file '$relPath' was changed. Update the related Docs/ specification files and the shared MemoryBank/ files as needed. At minimum, review activeContext.md and decisionLog.md, and update patterns.md or openQuestions.md when relevant. Report which Docs and MemoryBank files were updated."

@{
    hookSpecificOutput = @{
        hookEventName     = 'PostToolUse'
        additionalContext = $message
    }
} | ConvertTo-Json -Compress -Depth 10