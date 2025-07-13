![alt text](https://github.com/dangvd/crystal-remix-icon-theme/blob/main/128x128/places/folder-music.png?raw=true)
# neoPDF2Muse

neoPDF2Muse is a command-line tool that converts PDF files of sheet music into MusicXML 🎼 and MuseScore (.mscx) files. It leverages the power of the [*homr*](https://github.com/liebharc/homr) Python module to transcribe the music from the PDF.

## 🙏 Acknowledgements

This project would not have been possible without the excellent work done by the [*homr*](https://github.com/liebharc/homr) project. We extend our sincere gratitude to the *homr* team for creating such a powerful and versatile optical music recognition library.

## ⚙️ Dependencies

This project requires the following:

*   Python 3.10. 🐍
*   **Python Libraries:** 📚
    *   `homr`
    *   `pdf2image`
    *   `requests`
*   **External Tools:** 🛠️
    *   Poppler (for pdf to image conversion).

## ⬇️ Installation

1.  **Install Python:** Make sure you have Python 3.10 or higher installed. You can check your Python version by running `python --version` or `python3 --version` in your terminal.
2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/thurchito/neoPDF2Muse.git
    cd neoPDF2Muse
    ```
3.  **Run the Setup Script:** ⚙️
    Run the appropriate setup script for your operating system:
    *   **Linux/macOS:** `./setup.sh`
    *   **Windows:** `setup.bat`

    The setup script will:
    *   Install Miniconda locally within the `miniconda` directory.
    *   Prompt you to select an installation version: `CPU`, `GPU (ONNX Runtime)`, `TensorFlow GPU`, or `Gradio UI`.
    *   Create a Conda environment named `neoPDF2Muse` with the necessary dependencies.

## 🚀 Usage

1.  **Run the Run Script:** 🚀
    Run the appropriate run script for your operating system:
    *   **Linux/macOS:** `./run_pdf2muse.sh`
    *   **Windows:** `run_pdf2muse.bat`

    The run script will:
    *   Prompt you to select a runtime version: `CPU`, `GPU (ONNX Runtime)`, `TensorFlow GPU`, or `Gradio UI`.
    *   For `CPU`, `GPU`, and `TensorFlow GPU`:
        *   Prompt you for the path to the PDF file and the output directory (default: `output`).
        *   Run the neoPDF2Muse conversion process.
    *   For `Gradio UI`:
        *   Launch the Gradio web interface.

## 🧪 Testing

To test your installation, run the `run_pdf2muse.sh` or `run_pdf2muse.bat` script and select one of the runtime versions. Provide a sample PDF file and an output directory. Verify that the script completes successfully and generates the expected output files (MusicXML and MuseScore files). For the Gradio UI, verify that the web interface launches correctly and that you can upload a PDF file and convert it.

## 📜 Scripts

*   **`main.py`:** The main entry point of the application. It orchestrates the entire process: downloading checkpoints, converting PDF to PNG, running *homr*, joining MusicXML files, converting to MuseScore format, and cleaning up temporary files.
*   **`pdf_to_png.py`:** Converts each page of a PDF file into a separate PNG image using the `pdf2image` library (which depends on Poppler).
*   **`musicxml_utils.py`:** Provides utility functions for working with MusicXML files:
    *   `join_musicxml_files()`: Combines multiple MusicXML files (typically one per page) into a single MusicXML file.
    *   `convert_to_musescore_format()`: Converts a MusicXML file to the uncompressed MuseScore format (.mscx).

## 🛠️ Additional Notes

*   **Poppler:** Poppler is required for PDF to image conversion. The setup scripts will install it via Conda.
*   **CUDA (GPU Version):** The setup scripts will install CUDA 12.4 using `conda install nvidia/label/cuda-12.4.0::cuda-toolkit`.
