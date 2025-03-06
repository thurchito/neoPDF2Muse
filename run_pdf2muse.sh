#!/bin/bash

echo "Select runtime version:"
echo "1) CPU"
echo "2) GPU (ONNX Runtime)"
echo "3) TensorFlow GPU"
echo "4) Gradio UI"
read -p "Enter your choice (1-4): " choice

# Activate the Conda environment
source ./miniconda/bin/activate ./miniconda/envs/pdf2muse

case $choice in
    1)
        echo "Running with CPU..."
        read -p "Enter the path to the PDF file: " pdf_path
        read -p "Enter the output directory (default: output): " output_dir
        output_dir=${output_dir:-output}
        python main.py "$pdf_path" "$output_dir"
        ;;
    2)
        echo "Running with GPU (ONNX Runtime)..."
        read -p "Enter the path to the PDF file: " pdf_path
        read -p "Enter the output directory (default: output): " output_dir
        output_dir=${output_dir:-output}
        python main.py "$pdf_path" "$output_dir"
        ;;
    3)
        echo "Running with TensorFlow GPU..."
        read -p "Enter the path to the PDF file: " pdf_path
        read -p "Enter the output directory (default: output): " output_dir
        output_dir=${output_dir:-output}
        python main.py --use-tf "$pdf_path" "$output_dir"
        ;;
    4)
        echo "Running Gradio UI..."
        # Check if Gradio is installed
        if ! python -c "import gradio" 2>/dev/null; then
            echo "Gradio is not installed. Installing..."
            pip install gradio
        fi
        python gradio_app.py
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac
