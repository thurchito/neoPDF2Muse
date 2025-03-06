@echo off

REM Function to install Miniconda
:install_miniconda
echo "Installing Miniconda..."
set MINICONDA_DIR=miniconda
if exist "%MINICONDA_DIR%" (
    echo "Miniconda is already installed in %MINICONDA_DIR%."
    goto :eof
)

REM Download Miniconda installer
set MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
set MINICONDA_INSTALLER=Miniconda3-latest-Windows-x86_64.exe
curl -o "%MINICONDA_INSTALLER%" "%MINICONDA_URL%"

REM Silently install Miniconda
start /wait "" "%MINICONDA_INSTALLER%" /InstallationType=JustMe /RegisterPython=0 /S /D=%MINICONDA_DIR%
del "%MINICONDA_INSTALLER%"
goto :eof

REM Function to create Conda environment
:create_environment
set VERSION=%1
echo "Creating Conda environment for %VERSION%..."

if "%VERSION%"=="CPU" (
    set requirements_file=requirements-cpu.yml
) else if "%VERSION%"=="GPU" (
    set requirements_file=requirements-gpu.yml
) else if "%VERSION%"=="TensorFlow GPU" (
    set requirements_file=requirements-tf-gpu.yml"
) else if "%VERSION%"=="Gradio UI" (
    set requirements_file=requirements-cpu.yml  REM Use CPU dependencies as base for Gradio
) else (
    echo "Invalid version: %VERSION%"
    exit /b 1
)

.\miniconda\Scripts\conda.exe env create -f "%requirements_file%" -n pdf2muse --prefix .\miniconda\envs\pdf2muse
goto :eof

REM Main script logic
call :install_miniconda

echo "Select installation version:"
echo "1) CPU"
echo "2) GPU (ONNX Runtime)"
echo "3) TensorFlow GPU"
echo "4) Gradio UI"
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    call :create_environment "CPU"
) else if "%choice%"=="2" (
    call :create_environment "GPU"
) else if "%choice%"=="3" (
    call :create_environment "TensorFlow GPU"
) else if "%choice%"=="4" (
    call :create_environment "Gradio UI"
) else (
    echo "Invalid choice."
    exit /b 1
)

echo "Setup complete."

REM Download checkpoints after environment creation
.\miniconda\envs\pdf2muse\python.exe download_checkpoints.py
