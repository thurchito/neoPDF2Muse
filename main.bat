@echo off
start /wait /b "" "setup.bat"
:process
start /wait /b "" "run_pdf2muse.bat"
"zenity.exe" --list --title="neoPDF2Muse" --text="Would you like to process another file?" --radiolist --column="Check" --column="Options" "TRUE" "Yes, start new conversion;" "FALSE" "No, quit and clean up." --width=300 --height=180 > "%TEMP%\selection.tmp"
set /p choice=<"%TEMP%\selection.tmp"
del "%TEMP%\selection.tmp"
if "%choice%"=="Yes, start new conversion;" (
    goto :process
) else if "%choice%"=="No, quit and clean up." (
    exit
) else (
    exit
)
