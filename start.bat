@echo off
cd /d "%~dp0"

echo Starting obfuscator...
python ObfuscatorV2.py
if %errorlevel% neq 0 (
    echo.
    echo An error occurred while starting Obfuscator
    echo Error code: %errorlevel%
    exit /b %errorlevel%
)

echo.
echo Script executed successfully.
exit /b 0