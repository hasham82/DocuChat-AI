@echo off
echo ====================================
echo Starting RAG Chatbot (FREE)
echo ====================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Ollama is running
echo Checking Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama is not running!
    echo Please start Ollama or check system tray
    pause
    exit /b 1
)
echo [OK] Ollama is running
echo.

REM Start the application
echo Starting Streamlit application...
echo.
echo The chatbot will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
streamlit run app\streamlit_app.py