param(
  [Parameter(Mandatory=$true)][string]$Root,
  [Parameter(Mandatory=$true)][string[]]$RelativePath
)
$ErrorActionPreference = 'Stop'
$resolvedRoot = [System.IO.Path]::GetFullPath($Root).TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
$records = @()
foreach ($relative in $RelativePath) {
  if ([string]::IsNullOrWhiteSpace($relative) -or $relative.Contains('\') -or $relative.Contains(':') -or $relative.StartsWith('/') -or $relative.Contains([char]0)) { throw "STOP_UNSAFE_PATH:$relative" }
  $segments = $relative.Split('/')
  if ($segments | Where-Object { $_ -in @('', '.', '..') -or $_.EndsWith(' ') -or $_.EndsWith('.') }) { throw "STOP_UNSAFE_PATH:$relative" }
  $literal = [System.IO.Path]::GetFullPath((Join-Path $resolvedRoot ($relative.Replace('/', [System.IO.Path]::DirectorySeparatorChar))))
  if (-not $literal.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) { throw "STOP_OUTSIDE_ROOT:$relative" }
  $item = Get-Item -LiteralPath $literal -Force
  if ($item.PSIsContainer) { throw "STOP_EXPECTED_FILE:$relative" }
  if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0 -or $null -ne $item.LinkType) { throw "STOP_REPARSE_POINT:$relative" }
  $streams = @(Get-Item -LiteralPath $literal -Stream * | ForEach-Object Stream)
  if ($streams.Count -ne 1 -or $streams[0] -ne ':$DATA') { throw "STOP_ADS:$relative" }
  $hardlinkOutput = @(& fsutil hardlink list $literal 2>$null)
  if ($LASTEXITCODE -ne 0) { throw "STOP_HARDLINK_QUERY_FAILED:$relative" }
  $hardlinks = @($hardlinkOutput | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
  if ($hardlinks.Count -ne 1) { throw "STOP_HARDLINK:$relative" }
  $beforeLength = $item.Length
  $beforeWrite = $item.LastWriteTimeUtc.Ticks
  $stream = [System.IO.File]::Open($literal, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::Read)
  try {
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    try { $hash = ([System.BitConverter]::ToString($hasher.ComputeHash($stream))).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose() }
  }
  finally { $stream.Dispose() }
  $after = Get-Item -LiteralPath $literal -Force
  if ($after.Length -ne $beforeLength -or $after.LastWriteTimeUtc.Ticks -ne $beforeWrite) { throw "STOP_TOCTOU:$relative" }
  $records += [ordered]@{
    path = $relative
    final_path = $literal
    bytes = [int64]$after.Length
    sha256 = $hash
    attributes = [string]$after.Attributes
    stream_count = $streams.Count
    hardlink_count = $hardlinks.Count
    last_write_ticks = [int64]$after.LastWriteTimeUtc.Ticks
  }
}
[ordered]@{
  schema = 'n8nagents.windows-path-custody/v1'
  root = $resolvedRoot
  record_count = $records.Count
  records = $records
} | ConvertTo-Json -Depth 6 -Compress
