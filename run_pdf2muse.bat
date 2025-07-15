@echo off
echo [93mneoPDF2Muse v1.0[0m
echo:

start /wait /b "" "zenity.exe" --list --title="neoPDF2Muse" --text="Select runtime version:" --radiolist --column="Check" --column="Options" "FALSE" "CPU" "FALSE" "GPU (ONNX Runtime)" "FALSE" "TensorFlow GPU" "FALSE" "Gradio UI" --width=250 --height=250 > "%TEMP%\selection.tmp" 2>nul
set /p choice=<"%TEMP%\selection.tmp"
del "%TEMP%\selection.tmp"
if not defined choice goto :abort

REM Activate the Conda environment
call .\miniconda\Scripts\activate.bat .\miniconda\envs\neoPDF2Muse

start /b "" "zenity.exe" --info --title="neoPDF2Muse" --text="Configuring \"%choice%\" runtime..." --width=200 --height=50
ping localhost -n 5 >nul
call :fileselect
if "%pdf_path%"=="" goto :abort
if "%output_dir%"=="" goto :abort
start /b "" "zenity.exe" --info --title="neoPDF2Muse" --text="Processing; Please wait..." --width=180 --height=50
echo Initializing conversion...
if "%choice%"=="CPU" python main.py "%pdf_path%" "%output_dir%"
if "%choice%"=="GPU (ONNX Runtime)" python main.py "%pdf_path%" "%output_dir%"
if "%choice%"=="TensorFlow GPU" python main.py --use-tf "%pdf_path%" "%output_dir%"
if "%choice%"=="Gradio UI" (
    ping localhost -n 5 >nul
    taskkill /f /im zenity.exe >nul & start /b "" "zenity.exe" --info --title="neoPDF2Muse" --text="Configuring \"Gradio UI\" runtime..." --width=200 --height=50 2>nul
    REM Check if Gradio is installed in the active Conda environment
    python -c "import gradio" 2>NUL
    if errorlevel 1 (
        taskkill /f /im zenity.exe >nul & start /b "" "zenity.exe" --warning --title="neoPDF2Muse" --text="Gradio UI not found. Installing..." --width=200 --height=50 2>nul
        call pip install gradio
    )
    python gradio_app.py
)
taskkill /f /im zenity.exe >nul & start /b /wait "" "zenity.exe" --info --title="neoPDF2Muse" --text="Processing completed. Be sure to check the open 'cmd' window for possible ignored errors." --width=300 --height=50 2>nul
exit

:abort
start /wait /b "" "zenity.exe" --error --title="neoPDF2Muse" --text="Operation cancelled." --width=100 --height=50
endlocal
exit /b

:fileselect
    set "pdf_path="
    set "output_dir="

    taskkill /f /im zenity.exe >nul && start /wait /b "" "zenity.exe" --file-selection --title="Select the desired PDF file for conversion:" > "%TEMP%\selection.tmp" 2>nul
    set /p pdf_path=<"%TEMP%\selection.tmp"
    del "%TEMP%\selection.tmp"
    if not defined pdf_path (
        goto :abort
    )

    start /wait /b "" "zenity.exe" --file-selection --directory --title="Select the desired output directory:" > "%TEMP%\selection.tmp" 2>nul
    set /p output_dir=<"%TEMP%\selection.tmp"
    del "%TEMP%\selection.tmp"
    if not defined output_dir (
        goto :abort
    )
    for %%F in ("%pdf_path%") do echo %%~nxF > "%TEMP%\imgdirfull.tmp"
    set /p imgdirfull=<"%TEMP%\imgdirfull.tmp"
    for %%G in ("%imgdirfull%") do set "imgdir=%%~nG" >nul
    rmdir /s /q "%output_dir%\%imgdir%" >nul 2>&1
    exit /b
