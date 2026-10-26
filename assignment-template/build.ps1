param(
    [ValidateSet('main','example','code-demo','all')]
    [string]$Target = 'all'
)
$ErrorActionPreference = 'Stop'
$compiler = Get-Command latexmk -ErrorAction Stop
$documents = if ($Target -eq 'all') { @('main','example','code-demo') } else { @($Target) }
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Force -Path 'build' | Out-Null
    foreach ($document in $documents) {
        $consoleLog = Join-Path 'build' "$document-build.txt"
        # Windows PowerShell 5 treats native stderr as an ErrorRecord.
        # Capture it and use the compiler exit code to decide success.
        $ErrorActionPreference = 'Continue'
        try {
            & $compiler.Source '-xelatex' '-shell-escape' '-synctex=1' '-interaction=nonstopmode' `
                '-file-line-error' '-halt-on-error' '-outdir=build' "$document.tex" *> $consoleLog
            $compilerExit = $LASTEXITCODE
        } finally {
            $ErrorActionPreference = 'Stop'
        }
        if ($compilerExit -ne 0) {
            Get-Content -LiteralPath $consoleLog -Tail 40
            throw "Compilation failed. See $consoleLog."
        }
        Write-Output "Created build/$document.pdf"
    }
} finally {
    Pop-Location
}
