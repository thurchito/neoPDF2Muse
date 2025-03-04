import argparse
import logging
import os
import subprocess
import tempfile
import zipfile

import fitz  # PyMuPDF
from lxml import etree

def main():
    parser = argparse.ArgumentParser(description="Convert PDF scores to MuseScore formats using oemer.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input PDF file.")
    parser.add_argument("-o", "--output_dir", default=".", help="Path to the output directory (default: current directory).")
    parser.add_argument("-f", "--formats", nargs="+", default=["mscz"], choices=["mscz", "mscx", "mxl", "xml", "mid"], help="List of output formats (default: mscz).")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU usage for oemer (if available).")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        pdf_to_musescore(args.input, args.output_dir, args.formats, args.gpu)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def pdf_to_musescore(pdf_path, output_dir, output_formats, use_gpu):
    """
    Converts a PDF score to MuseScore formats.
    """
    logging.info(f"Processing PDF: {pdf_path}")

    with tempfile.TemporaryDirectory() as temp_dir:
        logging.info(f"Using temporary directory: {temp_dir}")

        # 1. PDF Processing: Extract images from PDF
        image_paths = extract_images_from_pdf(pdf_path, temp_dir)

        # 2. OMR Processing: Run oemer on each image
        musicxml_paths = perform_omr(image_paths, temp_dir, use_gpu)

        # 3. Convert MusicXML to .mscx
        mscx_paths = convert_musicxml_to_mscx_files(musicxml_paths, temp_dir)

        # 4. Output Format Generation
        generate_output_formats(mscx_paths, image_paths, output_dir, output_formats)

    logging.info("PDF processing complete.")

def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extracts images from a PDF file using PyMuPDF.
    """
    logging.info(f"Extracting images from PDF: {pdf_path}")
    image_paths = []
    try:
        pdf_document = fitz.open(pdf_path)
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # High-resolution extraction
            image_path = os.path.join(output_dir, f"page_{page_number + 1}.png")
            pix.save(image_path)
            image_paths.append(image_path)
        pdf_document.close()
    except Exception as e:
        logging.error(f"Error extracting images from PDF: {e}")
        return []
    logging.info(f"Extracted {len(image_paths)} images.")
    return image_paths

def perform_omr(image_paths, output_dir, use_gpu):
    """
    Performs OMR on a list of images using oemer.
    """
    logging.info("Performing OMR with oemer...")
    musicxml_paths = []
    for image_path in image_paths:
        try:
            output_path = os.path.join(output_dir)  # oemer determines the output filename
            command = ["oemer", image_path, "-o", output_path]
            if not use_gpu:
                command.append("--use-tf")  # Use TensorFlow (CPU)

            logging.info(f"Running oemer command: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            logging.info(f"oemer output: {result.stdout}")
            if result.stderr:
                logging.warning(f"oemer stderr: {result.stderr}")

            # Discover the MusicXML filename (oemer determines the name)
            musicxml_path = discover_musicxml_path(output_dir, image_path)
            if musicxml_path:
                musicxml_paths.append(musicxml_path)
            else:
                logging.error(f"Could not find MusicXML output for {image_path}")

        except subprocess.CalledProcessError as e:
            logging.error(f"Error during OMR processing: {e}")
            logging.error(f"oemer stderr: {e.stderr}")
        except Exception as e:
            logging.error(f"Error during OMR processing: {e}")
    logging.info(f"Generated {len(musicxml_paths)} MusicXML files.")
    return musicxml_paths

def discover_musicxml_path(output_dir, image_path):
    """
    Discovers the MusicXML output path based on the image path.
    """
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    musicxml_path = os.path.join(output_dir, f"{image_name}.musicxml")
    if os.path.exists(musicxml_path):
        return musicxml_path
    else:
        return None

def convert_musicxml_to_mscx_files(musicxml_paths, output_dir):
    """
    Converts MusicXML files to .mscx files.
    """
    logging.info("Converting MusicXML to .mscx...")
    mscx_paths = []
    for musicxml_path in musicxml_paths:
        try:
            mscx_path = os.path.splitext(os.path.basename(musicxml_path))[0] + ".mscx"
            mscx_path = os.path.join(output_dir, mscx_path)
            convert_musicxml_to_mscx(musicxml_path, mscx_path)
            mscx_paths.append(mscx_path)
        except Exception as e:
            logging.error(f"Error converting {musicxml_path} to .mscx: {e}")
    logging.info(f"Converted {len(mscx_paths)} MusicXML files to .mscx.")
    return mscx_paths

def convert_musicxml_to_mscx(musicxml_path, mscx_path):
    """
    Converts a MusicXML file to a .mscx file.
    """
    logging.info(f"Converting MusicXML: {musicxml_path} to .mscx: {mscx_path}")
    try:
        tree = etree.parse(musicxml_path)
        root = tree.getroot()

        # TODO: Implement MusicXML to .mscx conversion logic here
        # This is a placeholder - replace with actual conversion code
        # Example:
        # for note in root.findall(".//note"):
        #     pitch = note.find("pitch")
        #     if pitch is not None:
        #         step = pitch.find("step").text
        #         octave = pitch.find("octave").text
        #         logging.info(f"Note: {step}{octave}")

        # Create a dummy .mscx file for now
        with open(mscx_path, "w") as f:
            f.write("<!-- Dummy .mscx file -->\n<museScore version=\"3.0.0\">\n  <Score>\n    <Part>\n      <Staff>\n        <Measure>\n          <voice>\n            <Rest>\n              <durationType>whole</durationType>\n            </Rest>\n          </voice>\n        </Measure>\n      </Staff>\n    </Part>\n  </Score>\n</museScore>")

    except Exception as e:
        logging.error(f"Error parsing MusicXML: {e}")

def generate_output_formats(mscx_paths, image_paths, output_dir, output_formats):
    """
    Generates the specified output formats from the .mscx files.
    """
    logging.info(f"Generating output formats: {output_formats}")
    for mscx_path in mscx_paths:
        base_name = os.path.splitext(os.path.basename(mscx_path))[0]
        if "mscz" in output_formats:
            mscz_path = os.path.join(output_dir, base_name + ".mscz")
            create_mscz(mscx_path, os.path.dirname(image_paths[0]), mscz_path) # Assuming all images are in the same directory
        if "mxl" in output_formats:
            musicxml_path = os.path.splitext(mscx_path)[0] + ".musicxml" # Assuming musicxml has the same name as mscx
            mxl_path = os.path.join(output_dir, base_name + ".mxl")
            create_mxl(musicxml_path, mxl_path)
        if "xml" in output_formats:
            musicxml_path = os.path.splitext(mscx_path)[0] + ".musicxml" # Assuming musicxml has the same name as mscx
            xml_path = os.path.join(output_dir, base_name + ".xml")
            create_xml(musicxml_path, xml_path)
        if "mid" in output_formats:
            mid_path = os.path.join(output_dir, base_name + ".mid")
            create_midi(mscx_path, mid_path)

def create_mscz(mscx_path, images_dir, mscz_path):
    """
    Creates a .mscz file from a .mscx file and the extracted images.
    """
    logging.info(f"Creating .mscz: {mscz_path}")
    try:
        with zipfile.ZipFile(mscz_path, "w", zipfile.ZIP_DEFLATED) as mscz_file:
            mscz_file.write(mscx_path, os.path.basename(mscx_path))

            # Add images
            for image_path in os.listdir(images_dir):
                if image_path.endswith(".png"):
                    mscz_file.write(os.path.join(images_dir, image_path), image_path)

            # Add thumbnail (placeholder)
            # TODO: Generate a proper thumbnail
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_thumb:
                tmp_thumb.write(b"Dummy thumbnail data")  # Replace with actual thumbnail generation
                mscz_file.write(tmp_thumb.name, "Thumbnails/thumbnail.png")
                os.unlink(tmp_thumb.name)

            # Add metadata files (placeholders)
            # TODO: Create default metadata files
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_meta:
                tmp_meta.write("{}")
                mscz_file.write(tmp_meta.name, "audiosettings.json")
                os.unlink(tmp_meta.name)
            with tempfile.NamedTemporaryFile(mode="w", suffix=".mss", delete=False) as tmp_meta:
                tmp_meta.write("")
                mscz_file.write(tmp_meta.name, "score_style.mss")
                os.unlink(tmp_meta.name)
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_meta:
                tmp_meta.write("{}")
                mscz_file.write(tmp_meta.name, "viewsettings.json")
                os.unlink(tmp_meta.name)
            with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as tmp_meta:
                tmp_meta.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<manifest version=\"1.0\"></manifest>")
                mscz_file.write(tmp_meta.name, "META-INF/container.xml")
                os.unlink(tmp_meta.name)


    except Exception as e:
        logging.error(f"Error creating .mscz: {e}")

def create_mxl(musicxml_path, mxl_path):
    """
    Compresses a MusicXML file to create a .mxl file.
    """
    logging.info(f"Creating .mxl: {mxl_path}")
    try:
        with zipfile.ZipFile(mxl_path, "w", zipfile.ZIP_DEFLATED) as mxl_file:
            mxl_file.write(musicxml_path, os.path.basename(musicxml_path))
    except Exception as e:
        logging.error(f"Error creating .mxl: {e}")

def create_xml(musicxml_path, xml_path):
    """
    Saves a MusicXML file directly as a .xml file.
    """
    logging.info(f"Creating .xml: {xml_path}")
    try:
        os.rename(musicxml_path, xml_path)  # Simply rename the file
    except Exception as e:
        logging.error(f"Error creating .xml: {e}")

def create_midi(mscx_path, midi_path):
    """
    Converts a .mscx file to a MIDI file.
    """
    logging.info(f"Creating .mid: {midi_path}")
    try:
        # TODO: Implement .mscx to MIDI conversion using music21 or mido
        # This is a placeholder
        with open(midi_path, "w") as f:
            f.write("Dummy MIDI data")
    except Exception as e:
        logging.error(f"Error creating .mid: {e}")

if __name__ == "__main__":
    main()
