@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"

echo ========================================
echo Excel to Markdown Converter
echo ========================================
echo.

REM 1) Python needed (py launcher)
where /q py
if errorlevel 1 (
  echo [ERROR] Python "py" launcher not found.
  echo Install Python 3.12+ then retry.
  echo Example: winget install -e --id Python.Python.3.12
  pause
  exit /b 1
)

REM 2) Create venv (first time only)
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  py -3 -m venv ".venv"
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
  )
)

REM 3) Install deps (proxy fallback)
echo Activating virtual environment...
call ".venv\Scripts\activate.bat"

set "HTTP_PROXY=http://proxy2.ibis.intec.co.jp:8080"
set "HTTPS_PROXY=http://proxy2.ibis.intec.co.jp:8080"

echo.
echo ========================================
echo Installing dependencies...
echo ========================================
echo.

python -m pip install --upgrade pip --proxy "%HTTP_PROXY%" 2>nul || echo [WARNING] pip upgrade failed - continuing...

call :pip_with_proxy && goto :run
echo [WARNING] Proxy installation failed. Trying without proxy...
call :pip_without_proxy && goto :run
echo [WARNING] Standard installation failed. Trying --user installation...
call :pip_user && goto :run

echo [ERROR] All installation methods failed.
echo.
echo SOLUTIONS:
echo 1. Ask IT admin to configure proxy authentication
echo 2. Download wheel files from https://pypi.org/ and install offline
echo.
pause
exit /b 1

:run
echo.
echo ========================================
echo Running Excel to Markdown conversion...
echo ========================================
python excel2md_batch.py %*
set "RESULT=%errorlevel%"

echo.
echo ========================================
echo Conversion completed with exit code: %RESULT%
echo ========================================
pause
exit /b %RESULT%

:pip_with_proxy
pip install -r requirements.txt --proxy "%HTTP_PROXY%"
exit /b %errorlevel%

:pip_without_proxy
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
exit /b %errorlevel%

:pip_user
pip install --user openpyxl pandas tabulate python-docx
exit /b %errorlevel%
