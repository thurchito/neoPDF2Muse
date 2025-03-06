#!/bin/bash

# Function to install Miniconda
install_miniconda() {
    echo "Installing Miniconda..."
    MINICONDA_DIR="miniconda"
    if [ -d "$MINICONDA_DIR" ]; then
        echo "Miniconda is already installed in $MINICONDA_DIR."
        return
    fi

    # Determine OS and download appropriate Miniconda installer
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        MINICONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
        MINICONDA_INSTALLER="Miniconda3-latest-MacOSX-x86_64.sh"
    else
        echo "Unsupported OS: $OSTYPE"
        exit 1
    fi

    wget "$MINICONDA_URL" -O "$MINICONDA_INSTALLER"
    bash "$MINICONDA_INSTALLER" -b -p "$MINICONDA_DIR"
    rm "$MINICONDA_INSTALLER"
}

# Function to create Conda environment
create_environment() {
    VERSION=$1
    echo "Creating Conda environment for $VERSION..."
    case $VERSION in
        CPU)
            requirements_file="requirements-cpu.yml"
            ;;
        GPU)
            requirements_file="requirements-gpu.yml"
            ;;
        "TensorFlow GPU")
            requirements_file="requirements-tf-gpu.yml"
            ;;
        "Gradio UI")
            requirements_file="requirements-cpu.yml" # Use CPU dependencies as base for Gradio
            ;;
        *)
            echo "Invalid version: $VERSION"
            exit 1
            ;;
    esac

  ./miniconda/bin/conda env create -f "$requirements_file" -n pdf2muse --prefix ./miniconda/envs/pdf2muse
}

# Main script logic
install_miniconda

echo "Select installation version:"
echo "1) CPU"
echo "2) GPU (ONNX Runtime)"
echo "3) TensorFlow GPU"
echo "4) Gradio UI"
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        create_environment "CPU"
        ;;
    2)
        create_environment "GPU"
        ;;
    3)
        create_environment "TensorFlow GPU"
        ;;
    4)
        create_environment "Gradio UI"
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac
echo "Setup complete."

# Download checkpoints after environment creation
./miniconda/envs/pdf2muse/bin/python download_checkpoints.py
