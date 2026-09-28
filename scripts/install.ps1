# Link the active skills of this repository into a Claude Code skills directory.
#
#   powershell -File scripts\install.ps1                    -> ~\.claude\skills   (all projects)
#   powershell -File scripts\install.ps1 .\.claude\skills   -> one project only
#
# Uses directory junctions, which need neither admin rights nor Developer Mode.
# Links, not copies: `git pull` in this repo updates every installed skill.
# An existing folder with the same name is left alone and reported.
param([string]$Target = (Join-Path $HOME '.claude\skills'))

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
New-Item -ItemType Directory -Force -Path $Target | Out-Null

# Only the active set from .claude-plugin/plugin.json; core spokes load via promethean-parthenon.
$active = (Get-Content (Join-Path $root '.claude-plugin\plugin.json') -Raw | ConvertFrom-Json).skills | ForEach-Object { $_.TrimStart('.', '/') }

$active | ForEach-Object { Get-Item (Join-Path $root $_) } | ForEach-Object {
    $dest = Join-Path $Target $_.Name
    $existing = Get-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
    if ($existing) {
        if ($existing.LinkType) {
            $existing.Delete()
        } else {
            Write-Host "skip  $($_.Name) (already exists and is not a link)"
            return
        }
    }
    New-Item -ItemType Junction -Path $dest -Target $_.FullName | Out-Null
    Write-Host "link  $($_.Name)"
}
