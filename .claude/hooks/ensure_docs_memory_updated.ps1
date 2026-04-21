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

function Normalize-RepoPath([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path)) { return "" }
    $p = ($Path.Trim() -replace '\\', '/')
    while ($p.StartsWith('./')) {
        $p = $p.Substring(2)
    }
    return $p
}

$data = Read-HookInput
if ($data -and $data.stop_hook_active -eq $true) {
    exit 0
}

& git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) {
    exit 0
}

$changed = @()
$changed += @(& git diff --name-only HEAD -- 2>$null)
$changed += @(& git ls-files --others --exclude-standard 2>$null)

$changed = $changed |
    Where-Object { $_ -and $_.Trim() } |
    ForEach-Object { Normalize-RepoPath $_ } |
    Sort-Object -Unique

if (-not $changed -or $changed.Count -eq 0) {
    exit 0
}

$docsChanged = $false
$memoryChanged = $false
$nonMetaChanged = @()

foreach ($path in $changed) {
    $isDocs = $path.StartsWith('Docs/', [System.StringComparison]::OrdinalIgnoreCase) -or
              $path.StartsWith('docs/', [System.StringComparison]::OrdinalIgnoreCase)

    $isMemory = $path.StartsWith('MemoryBank/', [System.StringComparison]::OrdinalIgnoreCase) -or
                $path.StartsWith('memory-bank/', [System.StringComparison]::OrdinalIgnoreCase)

    $isClaude = $path.StartsWith('.claude/', [System.StringComparison]::OrdinalIgnoreCase)

    if ($isDocs) { $docsChanged = $true }
    if ($isMemory) { $memoryChanged = $true }

    if (-not $isDocs -and -not $isMemory -and -not $isClaude) {
        $nonMetaChanged += $path
    }
}

if ($nonMetaChanged.Count -gt 0) {
    $missing = @()
    if (-not $docsChanged)   { $missing += 'Docs/' }
    if (-not $memoryChanged) { $missing += 'MemoryBank/' }

    if ($missing.Count -gt 0) {
        $reason = "Code changes exist, but updates to {0} were not detected. Please update the related spec/docs and shared memory before finishing." -f ($missing -join ' and ')

        @{
            decision = 'block'
            reason   = $reason
        } | ConvertTo-Json -Compress -Depth 10

        exit 0
    }
}

exit 0