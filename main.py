import os
import sys
import shutil
import subprocess
from download_checkpoints import download_checkpoints
from pdf_to_png import pdf_to_png
from musicxml_utils import join_musicxml_files, convert_to_musescore_format

def main(pdf_path, output_dir):
    """
    Converts a PDF to MusicXML and MuseScore format using oemer.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the output files.
    """

    env_path = "C:/Users/djtri/miniconda3/envs/PDF2Muse"
    image_dir = os.path.join(output_dir, "images")
    musicxml_dir = os.path.join(output_dir, "musicxml")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(musicxml_dir, exist_ok=True)

    # Download checkpoints
    download_checkpoints(env_path)

    # Convert PDF to PNG images
    pdf_to_png(pdf_path, image_dir)

    # Run oemer on each PNG image
    for filename in os.listdir(image_dir):
        if filename.endswith(".png"):
            image_path = os.path.join(image_dir, filename)
            try:
                result = subprocess.run(
                    ["oemer", "--without-deskew", image_path],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                print(result.stdout)  # Print the output of oemer
                print(f"Successfully processed {filename}")
                # Move the musicxml file to the musicxml directory
                for file in os.listdir("."):
                    if file.endswith(".musicxml"):
                        shutil.move(file, musicxml_dir)

            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}: {e.stderr}")

    # Join the MusicXML files
    joined_musicxml_file = os.path.join(output_dir, "combined.musicxml")
    join_musicxml_files(musicxml_dir, joined_musicxml_file)

    # Convert to MuseScore format
    musescore_file = os.path.join(output_dir, "combined.mscx")
    convert_to_musescore_format(joined_musicxml_file, musescore_file, format="mscx")

    # Delete the image directory
    shutil.rmtree(image_dir)
    shutil.rmtree(musicxml_dir)

    print("PDF to MusicXML and MuseScore conversion complete!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <pdf_path> <output_dir>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]

    main(pdf_path, output_dir)
