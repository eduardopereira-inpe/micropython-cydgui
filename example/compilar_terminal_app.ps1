# Compilar todos os arquivos .py do pacote "cydgui" para .mpy usando mpy-cross
# Comando
#> Powershell -ExecutionPolicy Bypass -File .\compilar.ps1
# 1. Defina o nome da pasta do seu pacote principal
$nomeDoPacote = "terminal_app"

# 2. Define a pasta de saída
$pastaDestino = "${nomeDoPacote}_mpy\${nomeDoPacote}"

# 3. Limpa e recria a pasta de destino do zero
if (Test-Path $pastaDestino) { Remove-Item $pastaDestino -Recurse -Force }
$pastaDestinoAbsoluta = (New-Item -ItemType Directory -Path $pastaDestino).FullName
$pastaOrigemAbsoluta = (Get-Item $nomeDoPacote).FullName

# 4. Localiza todos os arquivos .py recursivamente
Get-ChildItem -Path $pastaOrigemAbsoluta -Filter *.py -Recurse | ForEach-Object {
    # Descobre o caminho relativo do arquivo em relação à pasta raiz do pacote
    $caminhoRelativo = $_.FullName.Substring($pastaOrigemAbsoluta.Length + 1)
    
    # Define a subpasta correspondente no destino
    $subPastaDestino = Split-Path $caminhoRelativo
    $pastaAlvoCompleta = Join-Path $pastaDestinoAbsoluta $subPastaDestino
    
    # Cria a árvore de subpastas no destino se ela ainda não existir
    if (-not (Test-Path $pastaAlvoCompleta)) { 
        New-Item -ItemType Directory -Path $pastaAlvoCompleta | Out-Null 
    }
    
    # Define o nome do arquivo final .mpy
    $arquivoMpy = Join-Path $pastaAlvoCompleta ($_.BaseName + ".mpy")
    
    # Compila o arquivo .py atual
    python -m mpy_cross $_.FullName -o $arquivoMpy
}

Write-Host "Sucesso! Estrutura de subpacotes compilada em: $pastaDestino" -ForegroundColor Green
