@echo off
setlocal
set "ASSIGNMENT_ROOT=%~dp0..\.."
"%ASSIGNMENT_ROOT%\.venv\Scripts\python.exe" -c "import latexminted; from pygments.styles import get_style_by_name; get_style_by_name('assignment-darcula')" >nul 2>nul
if errorlevel 1 (
    if not exist "%ASSIGNMENT_ROOT%\build" mkdir "%ASSIGNMENT_ROOT%\build"
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ASSIGNMENT_ROOT%\setup.ps1" > "%ASSIGNMENT_ROOT%\build\setup-log.txt" 2>&1
    if errorlevel 1 exit /b 1
)
"%ASSIGNMENT_ROOT%\.venv\Scripts\python.exe" -c "from latexminted.cmdline import main; main()" %*
exit /b %errorlevel%
