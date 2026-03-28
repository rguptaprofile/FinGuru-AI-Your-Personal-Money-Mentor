@echo off
REM ============================================================================
REM FinGuru AI - Video Recording Environment Setup Script
REM ============================================================================
REM This script prepares your environment for recording the 3-minute pitch video

echo.
echo ============================================================================
echo  FinGuru AI - 3-Minute Pitch Video Recording Setup
echo ============================================================================
echo.

REM Get project root
cd /d "%~dp0\.."
set PROJECT_ROOT=%cd%

echo [1/5] Checking project structure...
if exist "backend\app\main.py" (
    echo ✓ Backend found at: %PROJECT_ROOT%\backend
) else (
    echo ✗ Backend NOT found. Exiting.
    pause
    exit /b 1
)

if exist "frontend\package.json" (
    echo ✓ Frontend found at: %PROJECT_ROOT%\frontend
) else (
    echo ✗ Frontend NOT found. Exiting.
    pause
    exit /b 1
)

echo.
echo [2/5] Checking Python environment...
if exist "backend\.venv\Scripts\python.exe" (
    echo ✓ Virtual environment exists at: backend\.venv
    set PYTHON_EXE=%PROJECT_ROOT%\backend\.venv\Scripts\python.exe
) else (
    echo ⚠ Virtual environment NOT found. Creating now...
    cd backend
    python -m venv .venv
    cd ..
    set PYTHON_EXE=%PROJECT_ROOT%\backend\.venv\Scripts\python.exe
)

echo.
echo [3/5] Checking Node/npm...
where npm >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
    echo ✓ npm found (version %NPM_VERSION%)
) else (
    echo ✗ npm NOT found. Please install Node.js
    pause
    exit /b 1
)

echo.
echo [4/5] Checking frontend dependencies...
if exist "frontend\node_modules" (
    echo ✓ npm packages installed
) else (
    echo ⚠ npm packages NOT found. Installing now...
    cd frontend
    call npm install
    cd ..
)

echo.
echo [5/5] Recording environment ready!
echo.
echo ============================================================================
echo  NEXT STEPS - Run these commands in separate PowerShell windows:
echo ============================================================================
echo.
echo Window 1 (Backend):
echo ────────────────────────────────────────────────────────────────────────
echo   cd "%PROJECT_ROOT%"
echo   python -m uvicorn main:app --reload
echo.
echo   ✓ Backend will run on: http://127.0.0.1:8000
echo   ✓ API Docs available: http://127.0.0.1:8000/docs
echo.
echo Window 2 (Frontend):
echo ────────────────────────────────────────────────────────────────────────
echo   cd "%PROJECT_ROOT%"
echo   npm run dev
echo.
echo   ✓ Frontend will run on: http://localhost:3000
echo.
echo ============================================================================
echo  RECORDING CHECKLIST:
echo ============================================================================
echo.
echo Before pressing RECORD:
echo   □ Backend running on port 8000
echo   □ Frontend running on port 3000
echo   □ Browser open at http://localhost:3000
echo   □ OBS Studio configured with Display Capture
echo   □ Microphone levels tested (show green in OBS Mixer)
echo   □ Sample profile JSON ready
echo   □ TELEPROMPTER.txt open (docs\TELEPROMPTER.txt)
echo   □ Quiet recording environment
echo.
echo ============================================================================
echo  REFERENCE FILES:
echo ============================================================================
echo.
echo   📝 Teleprompter:        docs\TELEPROMPTER.txt
echo   📖 Full Guide:          docs\VIDEO-CREATION-GUIDE.md
echo   🎬 Pitch Script:        docs\pitch-video-script.md
echo   📊 Impact Numbers:      docs\impact-model.md
echo.
echo ============================================================================
echo.
echo Setup complete! Ready to record. Press any key to close this window.
echo.
pause
