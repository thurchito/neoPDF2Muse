@echo off

echo "Select runtime version:"
echo "1) CPU"
echo "2) GPU (ONNX Runtime)"
echo "3) TensorFlow GPU"
echo "4) Gradio UI"
set /p choice="Enter your choice (1-4): "

REM Activate the Conda environment
call .\miniconda\Scripts\activate.bat .\miniconda\envs\pdf2muse

if "%choice%"=="1" (
    echo "Running with CPU..."
    set /p pdf_path="Enter the path to the PDF file: "
    set /p "output_dir=Enter the output directory (default: output): "
    if "%output_dir%"=="" set output_dir=output
    python main.py "%pdf_path%" "%output_dir%"
) else if "%choice%"=="2" (
    echo "Running with GPU (ONNX Runtime)..."
    set /p pdf_path="Enter the path to the PDF file: "
    set /p "output_dir=Enter the output directory (default: output): "
    if "%output_dir%"=="" set output_dir=output
    python main.py "%pdf_path%" "%output_dir%"
) else if "%choice%"=="3" (
    echo "Running with TensorFlow GPU..."
    set /p pdf_path="Enter the path to the PDF file: "
    set /p "output_dir=Enter the output directory (default: output): "
    if "%output_dir%"=="" set output_dir=output
    python main.py --use-tf "%pdf_path%" "%output_dir%"
) else if "%choice%"=="4" (
    echo "Running Gradio UI..."
    REM Check if Gradio is installed
    python -c "import gradio" 2>NUL
    if errorlevel 1 (
        echo "Gradio is not installed. Installing..."
        pip install gradio
    )
    python gradio_app.py
) else (
    echo "Invalid choice."
    exit /b 1
)
