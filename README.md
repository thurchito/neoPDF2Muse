# PDF2Muse 🎶

PDF2Muse is a command-line tool that converts PDF files of sheet music into MusicXML 🎼 and MuseScore (.mscx) files. It leverages the power of the [oemer](https://github.com/BreezeWhite/oemer) optical music recognition library to transcribe the music from the PDF.

## 🙏 Acknowledgements

This project would not have been possible without the excellent work done by the [oemer](https://github.com/BreezeWhite/oemer) project. We extend our sincere gratitude to the oemer team for creating such a powerful and versatile optical music recognition library.

We also thank Google ☁️ for providing a free cloud trial, which enabled us to use the Gemini models and their awesomely large context window to "vibecode" this repository.

## 🏷️ Tags

`vibe-coding`, `optical-music-recognition`, `img2xml`

## ⚙️ Dependencies

This project requires the following:

*   Python 3.7+ 🐍
*   **Python Libraries:** 📚
    *   `oemer`
    *   `PyPDF2`
    *   `Pillow`
    *   `pdf2image`
    *   `requests`
*   **External Tools:** 🛠️
    *   Poppler (for pdf to image conversion, needs to be in system PATH)

## ⬇️ Installation

1.  **Install Python:** Make sure you have Python 3.7 or higher installed. You can check your Python version by running `python --version` or `python3 --version` in your terminal.
2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/thedivergentai/PDF2Muse.git
    cd PDF2Muse
    ```
3.  **Create and Activate a Virtual Environment (Recommended):** 🔒
    Creating a virtual environment isolates the project's dependencies.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On macOS/Linux
    .\.venv\Scripts\activate  # On Windows
    ```
4.  **Install Python Dependencies:** 📦
    ```bash
    pip install oemer PyPDF2 pdf2image requests Pillow
    ```
    Or, if you have a `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Install Poppler:** 📄
    *   **Windows:** Download and install Poppler for Windows from [a reliable source, e.g., a link to a known good installer - I will need to find a good link or ask the user]. Add the `bin` directory of your Poppler installation to your system's `PATH` environment variable.
    *   **macOS:** Install using Homebrew: `brew install poppler`
    *   **Linux:** Install using your distribution's package manager (e.g., `apt install poppler-utils` on Debian/Ubuntu).

## 🚀 Usage

The main script to run is `main.py`. It takes two arguments: the path to the input PDF and the output directory.

```bash
python main.py <pdf_path> <output_dir>
```

**Example:** 💡

```bash
python main.py my_sheet_music.pdf output
```

This will:

1.  Download the necessary oemer checkpoints (if they don't already exist).
2.  Convert the PDF (`my_sheet_music.pdf`) into a series of PNG images (one per page).
3.  Run oemer on each PNG image to generate individual MusicXML files.
4.  Combine the individual MusicXML files into a single `combined.musicxml` file.
5.  Convert the combined MusicXML file into a MuseScore file (`combined.mscx`).
6.  Save the final output in the `output` directory.
7.  Delete the intermediate PNG and individual MusicXML files.

## 📜 Scripts

*   **`main.py`:** The main entry point of the application. It orchestrates the entire process: downloading checkpoints, converting PDF to PNG, running oemer, joining MusicXML files, converting to MuseScore format, and cleaning up temporary files.
*   **`download_checkpoints.py`:** Handles downloading the pre-trained oemer model checkpoints if they are not already present in the expected location.
*   **`pdf_to_png.py`:** Converts each page of a PDF file into a separate PNG image using the `pdf2image` library (which depends on Poppler).
*   **`musicxml_utils.py`:** Provides utility functions for working with MusicXML files:
    *   `join_musicxml_files()`: Combines multiple MusicXML files (typically one per page) into a single MusicXML file.
    *   `convert_to_musescore_format()`: Converts a MusicXML file to the uncompressed MuseScore format (.mscx).
