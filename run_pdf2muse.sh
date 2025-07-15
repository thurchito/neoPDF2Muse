#!/bin/bash
echo -e "\033[1;33mneoPDF2Muse v1.0\033[0m"
echo ""

echo "Select runtime version:"
echo "1) CPU"
echo "2) GPU (ONNX Runtime)"
echo "3) TensorFlow GPU"
echo "4) Gradio UI"
read -p "Enter your choice (1-4): " choice

# Activate the Conda environment
source ./miniconda/bin/activate ./miniconda/envs/neoPDF2Muse

case $choice in
    1)
        echo "Configuring \"CPU\" runtime..."
        read -p "Enter the path to the PDF file: " pdf_path
        if [[ ! -f "$pdf_path" ]]; then
        echo "PDF file not found: $pdf_path"
        exit 1
        fi
        read -p "Enter the output directory (default: output): " output_dir
        output_dir="${output_dir:-output}"
        echo "Processing; Please wait..."
        echo "Initializing conversion..."
        tmp_file=$(mktemp)
        basename "$pdf_path" > "$tmp_file"
        imgdirfull=$(<"$tmp_file")
        imgdir="${imgdirfull%.*}"
        if [[ -d "$output_dir/$imgdir" ]]; then
        echo "Warning: Output directory '$output_dir/$imgdir' already exists. Deleting..."
        rm -rf "$output_dir/$imgdir"
        fi
        rm -f "$tmp_file"
        python main.py "$pdf_path" "$output_dir"
        ;;
    2)
        echo "Configuring \"GPU (ONNX)\" runtime..."
        read -p "Enter the path to the PDF file: " pdf_path
        if [[ ! -f "$pdf_path" ]]; then
        echo "PDF file not found: $pdf_path"
        exit 1
        fi
        read -p "Enter the output directory (default: output): " output_dir
        output_dir="${output_dir:-output}"
        echo "Processing; Please wait..."
        echo "Initializing conversion..."
        tmp_file=$(mktemp)
        basename "$pdf_path" > "$tmp_file"
        imgdirfull=$(<"$tmp_file")
        imgdir="${imgdirfull%.*}"
        if [[ -d "$output_dir/$imgdir" ]]; then
        echo "Warning: Output directory '$output_dir/$imgdir' already exists. Deleting..."
        rm -rf "$output_dir/$imgdir"
        fi
        rm -f "$tmp_file"
        python main.py "$pdf_path" "$output_dir"
        ;;
    3)
        echo "Configuring \"TensorFlow GPU\" runtime..."
        read -p "Enter the complete path to the PDF file: " pdf_path
        if [[ ! -f "$pdf_path" ]]; then
        echo "PDF file not found: $pdf_path"
        exit 1
        fi
        read -p "Enter the output directory (default: output): " output_dir
        output_dir="${output_dir:-output}"
        echo "Processing; Please wait..."
        echo "Initializing conversion..."
        tmp_file=$(mktemp)
        basename "$pdf_path" > "$tmp_file"
        imgdirfull=$(<"$tmp_file")
        imgdir="${imgdirfull%.*}"
        if [[ -d "$output_dir/$imgdir" ]]; then
        echo "Warning: Output directory '$output_dir/$imgdir' already exists. Deleting..."
        rm -rf "$output_dir/$imgdir"
        fi
        rm -f "$tmp_file"
        python main.py --use-tf "$pdf_path" "$output_dir"
        ;;
    4)
        echo "Configuring \"Gradio UI\"..."
        # Check if Gradio is installed
        if ! python -c "import gradio" 2>/dev/null; then
            echo "Gradio is not installed. Installing..."
            pip install gradio
        fi
        echo "Processing; Please wait..."
        python gradio_app.py
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac
