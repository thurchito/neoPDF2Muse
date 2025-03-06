# PDF2Muse 🎶

PDF2Muse is a command-line tool that converts PDF files of sheet music into MusicXML 🎼 and MuseScore (.mscx) files. It leverages the power of the [oemer](https://github.com/BreezeWhite/oemer) optical music recognition library to transcribe the music from the PDF.

## 🙏 Acknowledgements

This project would not have been possible without the excellent work done by the [oemer](https://github.com/BreezeWhite/oemer) project. We extend our sincere gratitude to the oemer team for creating such a powerful and versatile optical music recognition library.

We also thank Google ☁️ for providing a free cloud trial, which enabled us to use the Gemini models and their awesomely large context window to "vibecode" this repository.


## ⚙️ Dependencies

This project requires the following:

*   Python 3.9 🐍
*   **Python Libraries:** 📚
    *   `oemer`
    *   `pdf2image`
    *   `requests`
*   **External Tools:** 🛠️
    *   Poppler (for pdf to image conversion)

## ⬇️ Installation

1.  **Install Python:** Make sure you have Python 3.7 or higher installed. You can check your Python version by running `python --version` or `python3 --version` in your terminal.
2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/thedivergentai/PDF2Muse.git
    cd PDF2Muse
    ```
3.  **Run the Setup Script:** ⚙️
    Run the appropriate setup script for your operating system:
    *   **Linux/macOS:** `./setup.sh`
    *   **Windows:** `setup.bat`

    The setup script will:
    *   Install Miniconda locally within the `miniconda` directory.
    *   Prompt you to select an installation version: `CPU`, `GPU (ONNX Runtime)`, `TensorFlow GPU`, or `Gradio UI`.
    *   Create a Conda environment named `pdf2muse` with the necessary dependencies.

## 🚀 Usage

1.  **Run the Run Script:** 🚀
    Run the appropriate run script for your operating system:
    *   **Linux/macOS:** `./run_pdf2muse.sh`
    *   **Windows:** `run_pdf2muse.bat`

    The run script will:
    *   Prompt you to select a runtime version: `CPU`, `GPU (ONNX Runtime)`, `TensorFlow GPU`, or `Gradio UI`.
    *   For `CPU`, `GPU`, and `TensorFlow GPU`:
        *   Prompt you for the path to the PDF file and the output directory (default: `output`).
        *   Run the PDF2Muse conversion process.
    *   For `Gradio UI`:
        *   Launch the Gradio web interface.

## 🧪 Testing

To test your installation, run the `run_pdf2muse.sh` or `run_pdf2muse.bat` script and select one of the runtime versions. Provide a sample PDF file and an output directory. Verify that the script completes successfully and generates the expected output files (MusicXML and MuseScore files). For the Gradio UI, verify that the web interface launches correctly and that you can upload a PDF file and convert it.

## 📜 Scripts

*   **`main.py`:** The main entry point of the application. It orchestrates the entire process: downloading checkpoints, converting PDF to PNG, running oemer, joining MusicXML files, converting to MuseScore format, and cleaning up temporary files.
*   **`download_checkpoints.py`:** Handles downloading the pre-trained oemer model checkpoints if they are not already present in the expected location.
*   **`pdf_to_png.py`:** Converts each page of a PDF file into a separate PNG image using the `pdf2image` library (which depends on Poppler).
*   **`musicxml_utils.py`:** Provides utility functions for working with MusicXML files:
    *   `join_musicxml_files()`: Combines multiple MusicXML files (typically one per page) into a single MusicXML file.
    *   `convert_to_musescore_format()`: Converts a MusicXML file to the uncompressed MuseScore format (.mscx).

## 🛠️ Additional Notes

*   **Poppler:** Poppler is required for PDF to image conversion. The setup scripts will install it via Conda.
*   **CUDA (GPU Version):** The setup scripts will install CUDA 12.4 using `conda install nvidia/label/cuda-12.4.0::cuda-toolkit`.
