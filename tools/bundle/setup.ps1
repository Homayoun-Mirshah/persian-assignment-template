param([string]$Python = '', [switch]$Recreate)
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$venvPath = Join-Path $projectRoot '.venv'
$venvPython = Join-Path $venvPath 'Scripts\python.exe'
$wheelhouse = Join-Path $projectRoot 'wheelhouse'
$probe = "import latexminted, pygments, latex2pydata, latexrestricted, markdown, setuptools, wheel; from pygments.styles import get_style_by_name; [get_style_by_name(x) for x in ('assignment-darcula','assignment-intellij','assignment-vscode-dark','assignment-matlab')]"

function Test-ReadyPython([string]$candidate, [string]$code) {
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { return $false }
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try { & $candidate '-c' $code *> $null; return ($LASTEXITCODE -eq 0) }
    finally { $ErrorActionPreference = $oldPreference }
}

if (-not $Recreate -and (Test-ReadyPython $venvPython $probe)) {
    Write-Output 'The bundled Python environment is ready.'
    exit 0
}
if (-not (Test-Path -LiteralPath $wheelhouse -PathType Container)) {
    throw 'wheelhouse is missing. Extract the complete bundled package.'
}

$candidates = @()
if ($Python) {
    $requested = Get-Command $Python -ErrorAction SilentlyContinue
    if ($requested) { $candidates += $requested.Source }
    elseif (Test-Path -LiteralPath $Python) { $candidates += $Python }
    else { throw "Python executable not found: $Python" }
} else {
    foreach ($commandName in @('python','python3')) {
        $resolved = Get-Command $commandName -ErrorAction SilentlyContinue
        if ($resolved) { $candidates += $resolved.Source }
    }
    $appdataPaths = @($env:LOCALAPPDATA, (Join-Path $env:USERPROFILE 'AppData\Local'))
    foreach ($appdataPath in $appdataPaths) {
        if (-not $appdataPath) { continue }
        foreach ($pattern in @('Python\pythoncore-*\python.exe','Programs\Python\Python*\python.exe')) {
            $candidates += @(Get-ChildItem -Path (Join-Path $appdataPath $pattern) -File -ErrorAction SilentlyContinue |
                Sort-Object FullName -Descending | ForEach-Object FullName)
        }
    }
    $launcher = Get-Command py -ErrorAction SilentlyContinue
    if ($launcher) {
        $oldPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            $launcherResult = & $launcher.Source '-3' '-c' 'import sys; print(sys.executable)' 2>$null
            if ($LASTEXITCODE -eq 0) { $candidates += @($launcherResult) }
        } finally { $ErrorActionPreference = $oldPreference }
    }
}
$basePython = $null
foreach ($candidate in ($candidates | Select-Object -Unique)) {
    if (Test-ReadyPython $candidate 'import sys,venv; assert sys.version_info >= (3,9)') {
        $basePython = $candidate
        break
    }
}
if (-not $basePython) { throw 'Python 3.9+ with venv is required. Run setup.cmd -Python "C:\path\to\python.exe".' }

# venv is disposable, but always validate the exact target before recreating it.
$resolvedVenv = [IO.Path]::GetFullPath($venvPath)
if ($resolvedVenv -ne (Join-Path $projectRoot '.venv')) { throw 'Unexpected virtual-environment path.' }
$localTemp = Join-Path $projectRoot 'tmp\setup'
New-Item -ItemType Directory -Force -Path $localTemp | Out-Null
$previousTemp = $env:TEMP
$previousTmp = $env:TMP
$previousPipVersionCheck = $env:PIP_DISABLE_PIP_VERSION_CHECK
try {
    $env:TEMP = $localTemp
    $env:TMP = $localTemp
    $env:PIP_DISABLE_PIP_VERSION_CHECK = '1'
    & $basePython '-m' 'venv' '--clear' $resolvedVenv
    if ($LASTEXITCODE -ne 0) { throw 'Unable to create the Python virtual environment.' }
    & $venvPython '-m' 'pip' 'install' '--no-index' '--no-cache-dir' '--find-links' $wheelhouse `
        '-r' (Join-Path $projectRoot 'tools\requirements.txt') `
        '-r' (Join-Path $projectRoot 'tools\requirements-docs.txt') 'assignment-editorstyles==1.1.0'
    if ($LASTEXITCODE -ne 0) { throw 'Offline installation from wheelhouse failed.' }
    if (-not (Test-ReadyPython $venvPython $probe)) { throw 'Bundled package verification failed.' }
    Write-Output 'Bundled environment installed offline. Run build.cmd or compile main.tex in TeXstudio.'
} finally {
    $env:TEMP = $previousTemp
    $env:TMP = $previousTmp
    $env:PIP_DISABLE_PIP_VERSION_CHECK = $previousPipVersionCheck
}
