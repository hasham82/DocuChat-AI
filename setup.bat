@echo off
echo ====================================
echo RAG Chatbot Setup Script (FREE)
echo ====================================
echo.

REM Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.12 from https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo [OK] Python found!
echo.

REM Check Ollama
echo [2/6] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama not found!
    echo Please install Ollama from https://ollama.ai
    pause
    exit /b 1
)
ollama --version
echo [OK] Ollama found!
echo.

REM Check for Ollama model
echo [3/6] Checking Ollama models...
ollama list | findstr "llama3.1" >nul 2>&1
if errorlevel 1 (
    ollama list | findstr "mistral" >nul 2>&1
    if errorlevel 1 (
        ollama list | findstr "phi3" >nul 2>&1
        if errorlevel 1 (
            echo [WARNING] No models found!
            echo.
            echo Please download a model. Choose one:
            echo 1. ollama pull llama3.1    (Recommended, 4.7GB)
            echo 2. ollama pull mistral     (Fast, 4.1GB)
            echo 3. ollama pull phi3        (Fastest, 2.3GB)
            echo.
            set /p choice="Enter your choice (1-3): "
            if "%choice%"=="1" (
                echo Downloading llama3.1...
                ollama pull llama3.1
            ) else if "%choice%"=="2" (
                echo Downloading mistral...
                ollama pull mistral
            ) else if "%choice%"=="3" (
                echo Downloading phi3...
                ollama pull phi3
            ) else (
                echo Invalid choice. Please run setup again.
                pause
                exit /b 1
            )
        ) else (
            echo [OK] Found phi3 model
        )
    ) else (
        echo [OK] Found mistral model
    )
) else (
    echo [OK] Found llama3.1 model
)
echo.

REM Create virtual environment
echo [4/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo [OK] Virtual environment created!
)
echo.

REM Activate and install packages
echo [5/6] Installing Python packages...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo [OK] Packages installed!
echo.

REM Create folders
echo [6/6] Creating project folders...
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed
if not exist "chroma_db" mkdir chroma_db
echo [OK] Folders created!
echo.

REM Create sample document
if not exist "data\raw\sample.txt" (
    echo Creating sample document...
    (
        echo Introduction to Python Programming
        echo.
        echo Python is a high-level programming language created by Guido van Rossum.
        echo It was first released in 1991 and is known for its simplicity and readability.
        echo.
        echo Key Features:
        echo - Easy to learn
        echo - Large standard library
        echo - Cross-platform
        echo - Active community
        echo.
        echo Python is widely used in web development, data science, automation, and AI.
    ) > data\raw\sample.txt
    echo [OK] Sample document created!
)
echo.

echo ====================================
echo Setup Complete! ✓
echo ====================================
echo.
echo Next steps:
echo 1. Keep this window open OR open a new terminal
echo 2. Run: venv\Scripts\activate
echo 3. Run: streamlit run app\streamlit_app.py
echo.
echo The chatbot will open in your browser!
echo.
pause