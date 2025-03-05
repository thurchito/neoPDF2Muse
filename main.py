import os
import sys
import shutil
import subprocess
from download_checkpoints import download_checkpoints
from pdf_to_png import pdf_to_png

def main(pdf_path, output_dir):
    """
    Converts a PDF to MusicXML using oemer.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the MusicXML file.
    """

    env_path = "C:/Users/djtri/miniconda3/envs/PDF2Muse"
    image_dir = os.path.join(output_dir, "images")

    # Download checkpoints
    download_checkpoints(env_path)

    # Convert PDF to PNG images
    pdf_to_png(pdf_path, image_dir)

    # Run oemer on each PNG image
    for filename in os.listdir(image_dir):
        if filename.endswith(".png"):
            image_path = os.path.join(image_dir, filename)
            try:
                subprocess.run(["oemer", "--without-deskew", image_path], check=True, capture_output=True, text=True)
                print(f"Successfully processed {filename}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}: {e.stderr}")

    # Move MusicXML files to output directory and delete images
    for filename in os.listdir("."):
        if filename.endswith(".musicxml"):
            shutil.move(filename, output_dir)
    shutil.rmtree(image_dir)

    print("PDF to MusicXML conversion complete!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <pdf_path> <output_dir>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]

    main(pdf_path, output_dir)
