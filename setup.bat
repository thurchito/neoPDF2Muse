cmd /k
@echo off
SETLOCAL DisableDelayedExpansion

REM Function to install Miniconda
:install_miniconda
ECHO. "Installing Miniconda..."
set MINICONDA_DIR=miniconda
if exist "%MINICONDA_DIR%" (
    ECHO. "Miniconda is already installed in %MINICONDA_DIR%."
    goto :eof
)

REM Download Miniconda installer
set MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
set MINICONDA_INSTALLER=Miniconda3-latest-Windows-x86_64.exe
curl -o "%MINICONDA_INSTALLER%" "%MINICONDA_URL%"

REM Silently install Miniconda
start /wait "" "%MINICONDA_INSTALLER%" /InstallationType=JustMe /RegisterPython=0 /S /D=%CD%\%MINICONDA_DIR%
del "%MINICONDA_INSTALLER%"
timeout /t 10 /nobreak > nul
goto :eof

REM Function to create Conda environment
:create_environment
set VERSION=%1
ECHO. "Creating Conda environment for %VERSION%..."

if "%VERSION%"=="CPU" (
    set requirements_file=requirements-cpu.yml
) else if "%VERSION%"=="GPU" (
    set requirements_file=requirements-gpu.yml
) else if "%VERSION%"=="TensorFlow GPU" (
    set requirements_file=requirements-tf-gpu.yml"
) else if "%VERSION%"=="Gradio UI" (
    set requirements_file=requirements-cpu.yml  REM Use CPU dependencies as base for Gradio
) else (
    ECHO. "Invalid version: %VERSION%"
    exit /b 1
)

.\miniconda\Scripts\conda.exe env create -f "%requirements_file%" -n pdf2muse --prefix .\miniconda\envs\pdf2muse
goto :eof

REM Main script logic
call :install_miniconda

if not exist "%MINICONDA_DIR%" (
    ECHO. "Error: Miniconda installation failed. The directory %MINICONDA_DIR% does not exist."
    exit /b 1
)

ECHO. "Select installation version:"
ECHO. "1) CPU"
ECHO. "2) GPU (ONNX Runtime)"
ECHO. "3) TensorFlow GPU"
set /p choice="Enter your choice (1-3): "

ECHO. "Before calling create_environment"

if "%choice%"=="1" (
    set VERSION=CPU
) else if "%choice%"=="2" (
    set VERSION=GPU
) else if "%choice%"=="3" (
    set VERSION="TensorFlow GPU"
) else (
    ECHO. "Invalid choice."
    exit /b 1
)

ECHO. "After setting VERSION, VERSION is %VERSION%"

if defined VERSION call :create_environment "%VERSION%"

ECHO. "Setup complete."

REM Download checkpoints after environment creation
if defined VERSION .\miniconda\envs\pdf2muse\python.exe download_checkpoints.py
