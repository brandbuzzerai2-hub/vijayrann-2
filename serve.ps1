# The Vijayran Palace - local preview server (Windows PowerShell, nothing to install)
# - stops any earlier copy of this server first
# - serves several requests at once (video streaming never blocks pages/scripts)
param([int]$Port = 8080)
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1) stop older instances of this server
# (skipped to prevent killing runner process)

# 2) start listener (falls back to the next free port)
$listener = $null
for ($p = $Port; $p -le $Port + 20; $p++) {
  try { $l = New-Object System.Net.HttpListener; $l.Prefixes.Add("http://localhost:$p/"); $l.Start(); $listener = $l; $Port = $p; break } catch { }
}
if (-not $listener) { Write-Host "Could not open a port between 8080 and 8100." -ForegroundColor Red; exit 1 }
$url = "http://localhost:$Port/"
Write-Host ""; Write-Host "  The Vijayran Palace is running at $url" -ForegroundColor Yellow
Write-Host "  Keep this window open while you browse. Close it to stop the server."; Write-Host ""
Start-Process $url

# 3) request handler, run on a pool of threads
$handler = {
  param($ctx, $root)
  $types = @{ '.html'='text/html; charset=utf-8'; '.css'='text/css; charset=utf-8'; '.js'='application/javascript; charset=utf-8'; '.json'='application/json';
    '.png'='image/png'; '.jpg'='image/jpeg'; '.jpeg'='image/jpeg'; '.webp'='image/webp'; '.svg'='image/svg+xml'; '.gif'='image/gif';
    '.mp4'='video/mp4'; '.xml'='application/xml'; '.txt'='text/plain'; '.ico'='image/x-icon'; '.avif'='image/avif'; '.md'='text/plain; charset=utf-8' }
  $req = $ctx.Request; $res = $ctx.Response
  try {
    $res.AddHeader('Cache-Control','no-cache')
    $path = [Uri]::UnescapeDataString($req.Url.AbsolutePath).TrimStart('/')
    $file = Join-Path $root $path
    if ((Test-Path -LiteralPath $file -PathType Container) -or $path -eq '') { $file = Join-Path $file 'index.html' }
    $full = [IO.Path]::GetFullPath($file)
    if (-not $full.StartsWith([IO.Path]::GetFullPath($root), [System.StringComparison]::OrdinalIgnoreCase) -or -not (Test-Path -LiteralPath $full -PathType Leaf)) {
      $res.StatusCode = 404; $b = [Text.Encoding]::UTF8.GetBytes('404 Not Found'); $res.OutputStream.Write($b, 0, $b.Length); return
    }
    $ext = [IO.Path]::GetExtension($full).ToLower()
    $res.ContentType = $(if ($types.ContainsKey($ext)) { $types[$ext] } else { 'application/octet-stream' })
    $fs = [IO.File]::Open($full, 'Open', 'Read', 'ReadWrite')
    try {
      $len = $fs.Length; $start = 0; $end = $len - 1
      $range = $req.Headers['Range']
      if ($range -and $range -match 'bytes=(\d*)-(\d*)') {
        if ($matches[1]) { $start = [long]$matches[1] }
        if ($matches[2]) { $end = [long]$matches[2] }
        if ($end -ge $len) { $end = $len - 1 }
        if (($end - $start) -gt 2097151) { $end = $start + 2097151 }
        $res.StatusCode = 206; $res.AddHeader('Content-Range', "bytes $start-$end/$len")
      }
      $res.AddHeader('Accept-Ranges', 'bytes')
      $res.ContentLength64 = $end - $start + 1
      if ($req.HttpMethod -ne 'HEAD') {
        [void]$fs.Seek($start, 'Begin')
        $buf = New-Object byte[] 65536; $left = $res.ContentLength64
        while ($left -gt 0) { $n = $fs.Read($buf, 0, [int][Math]::Min($buf.Length, $left)); if ($n -le 0) { break }; $res.OutputStream.Write($buf, 0, $n); $left -= $n }
      }
    } finally { $fs.Close() }
  } catch { } finally { try { $res.OutputStream.Close() } catch { } }
}

$pool = [RunspaceFactory]::CreateRunspacePool(1, 16); $pool.Open()
$jobs = New-Object System.Collections.ArrayList
while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  $ps = [PowerShell]::Create(); $ps.RunspacePool = $pool
  [void]$ps.AddScript($handler).AddArgument($ctx).AddArgument($root)
  [void]$jobs.Add(@{ ps = $ps; h = $ps.BeginInvoke() })
  for ($i = $jobs.Count - 1; $i -ge 0; $i--) { if ($jobs[$i].h.IsCompleted) { try { $jobs[$i].ps.EndInvoke($jobs[$i].h) } catch {}; $jobs[$i].ps.Dispose(); $jobs.RemoveAt($i) } }
}
