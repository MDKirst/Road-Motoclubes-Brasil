# Servidorzinho local para jogar o Couro & Asfalto sem instalar nada.
# O navegador não deixa o jogo ler os arquivos da pista abrindo o index.html direto (file://),
# então este script serve a pasta "jogo" em http://localhost:8277 e abre o navegador.
# Só atende o próprio computador (localhost). Feche esta janela para desligar.
$ErrorActionPreference = 'Stop'
$porta = 8277
$raiz = Join-Path $PSScriptRoot 'jogo'
$tipos = @{
  '.html' = 'text/html; charset=utf-8'; '.js' = 'text/javascript; charset=utf-8'; '.css' = 'text/css; charset=utf-8'
  '.json' = 'application/json; charset=utf-8'; '.txt' = 'text/plain; charset=utf-8'; '.svg' = 'image/svg+xml'
  '.png' = 'image/png'; '.jpg' = 'image/jpeg'; '.jpeg' = 'image/jpeg'; '.webp' = 'image/webp'; '.gif' = 'image/gif'
  '.glb' = 'model/gltf-binary'; '.mp3' = 'audio/mpeg'; '.ogg' = 'audio/ogg'; '.wasm' = 'application/wasm'; '.ico' = 'image/x-icon'
}

$ouvinte = New-Object System.Net.HttpListener
$ouvinte.Prefixes.Add("http://localhost:$porta/")
try { $ouvinte.Start() } catch {
  Write-Host "Nao consegui abrir a porta $porta (talvez o jogo ja esteja aberto em outra janela)." -ForegroundColor Yellow
  Start-Process "http://localhost:$porta/"
  Read-Host 'Enter para fechar'
  exit
}
Write-Host ''
Write-Host '  COURO & ASFALTO - BR-277' -ForegroundColor Yellow
Write-Host "  Jogo aberto em http://localhost:$porta"
Write-Host '  Deixe esta janela aberta enquanto joga. Feche-a para desligar.'
Write-Host ''
if (-not $env:COURO_SEM_NAVEGADOR) { Start-Process "http://localhost:$porta/" } # (variável só para teste)

$raizCheia = [System.IO.Path]::GetFullPath($raiz)
while ($ouvinte.IsListening) {
  $ctx = $ouvinte.GetContext()
  $resp = $ctx.Response
  try {
    $caminho = [System.Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath).TrimStart('/')
    if ($caminho -eq '' -or $caminho.EndsWith('/')) { $caminho += 'index.html' }
    $arquivo = [System.IO.Path]::GetFullPath((Join-Path $raiz $caminho))
    # nunca sai da pasta do jogo
    if (-not $arquivo.StartsWith($raizCheia, [System.StringComparison]::OrdinalIgnoreCase) -or -not (Test-Path -LiteralPath $arquivo -PathType Leaf)) {
      $resp.StatusCode = 404
      $bytes = [System.Text.Encoding]::UTF8.GetBytes('nao encontrado')
    } else {
      $ext = [System.IO.Path]::GetExtension($arquivo).ToLowerInvariant()
      $resp.ContentType = if ($tipos.ContainsKey($ext)) { $tipos[$ext] } else { 'application/octet-stream' }
      $bytes = [System.IO.File]::ReadAllBytes($arquivo)
    }
    $resp.ContentLength64 = $bytes.Length
    $resp.OutputStream.Write($bytes, 0, $bytes.Length)
  } catch {
    try { $resp.StatusCode = 500 } catch {}
  } finally {
    try { $resp.OutputStream.Close() } catch {}
  }
}
