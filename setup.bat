@echo off
echo [93mneoPDF2Muse v1.0[0m
SETLOCAL DisableDelayedExpansion
goto :main

REM Function to install Miniconda
:install_miniconda
start /b "" "zenity.exe" --info --title="neoPDF2Muse" --text="Installing Miniconda..." --width=100 --height=50
ping localhost -n 5 >nul
set MINICONDA_DIR=miniconda
if exist "%MINICONDA_DIR%" (
	taskkill /f /im zenity.exe >nul & start /b /wait "" "zenity.exe" --warning --title="neoPDF2Muse" --text="Miniconda is already installed in \"%MINICONDA_DIR%.\"" --width=200 --height=50
	exit
)

REM Download Miniconda installer
set MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
set MINICONDA_INSTALLER=Miniconda3-latest-Windows-x86_64.exe
aria2c.exe -o "%MINICONDA_INSTALLER%" "%MINICONDA_URL%"

REM Silently install Miniconda
start /b /wait /MIN "" "%MINICONDA_INSTALLER%" /InstallationType=JustMe /RegisterPython=0 /S /D=%CD%\%MINICONDA_DIR%
del "%MINICONDA_INSTALLER%"
timeout /t 10 /nobreak > nul
exit /b

REM Function to create Conda environment
:create_environment
set VERSION=%1
ping localhost -n 5 >nul
taskkill /f /im zenity.exe >nul & start /b "" "zenity.exe" --info --title="neoPDF2Muse" --text="Creating Conda environment for \"%VERSION%\"..." --width=200 --height=50

if "%VERSION%"=="CPU" (
    set requirements_file=requirements-cpu.yml
) else if "%VERSION%"=="GPU" (
    set requirements_file=requirements-gpu.yml
) else if "%VERSION%"=="TensorFlow GPU" (
    set requirements_file=requirements-tf-gpu.yml
) else if "%VERSION%"=="Gradio UI" (
    set requirements_file=requirements-cpu.yml  REM Use CPU dependencies as base for Gradio
) else (
    taskkill /f /im zenity.exe >nul & start /b /wait "" "zenity.exe" --error --title="neoPDF2Muse" --text="Invalid version: \"%VERSION%\"" --width=100 --height=50  
    exit
)

.\miniconda\Scripts\conda.exe env create -f "%requirements_file%" --prefix .\miniconda\envs\neoPDF2Muse
exit /b

REM Main script logic
:main
call :install_miniconda

if not exist "%MINICONDA_DIR%" (
    taskkill /f /im zenity.exe >nul & start /b /wait "" "zenity.exe" --error --title="neoPDF2Muse" --text="Error: Miniconda installation failed. The directory \"%MINICONDA_DIR%\" does not exist. Are you connected to the internet?" --width=300 --height=50
    exit
)

taskkill /f /im zenity.exe >nul & start /b /wait "" "zenity.exe" --list --title="neoPDF2Muse" --text="Select installation version:" --radiolist --column="Check" --column="Options" "Option1" "CPU" "Option2" "GPU (ONNX Runtime)" "Option3" "TensorFlow GPU" --width=225 --height=225 > "%TEMP%\selection.tmp"
set /p choice=<"%TEMP%\selection.tmp"
del "%TEMP%\selection.tmp"

if "%choice%"=="CPU" (
    set VERSION=CPU
) else if "%choice%"=="GPU (ONNX Runtime)" (
    set VERSION=GPU
) else if "%choice%"=="TensorFlow GPU" (
    set VERSION="TensorFlow GPU"
) else (
     start /b "" "zenity.exe" --warning --title="neoPDF2Muse" --text="Setup halted. Reverting changes..." --width=100 --height=50
     rd /s /q %CD%\%MINICONDA_DIR% & taskkill /f /im zenity.exe
     exit
)

start /b "" "zenity.exe" --info --title="neoPDF2Muse" --text="Version set to \"%VERSION%\"." --width=175 --height=50
if defined VERSION call :create_environment %VERSION%
taskkill /f /im zenity.exe >nul & start /b /wait "" "zenity.exe" --info --title="neoPDF2Muse" --text="Setup completed. Be sure to check the open 'cmd' window for possible ignored errors." --width=300 --height=50
exit

