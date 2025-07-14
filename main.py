import os
import sys
import shutil
import subprocess
import argparse
from pdf_to_png import pdf_to_png
from musicxml_utils import join_musicxml_files, convert_to_musescore_format

def main(pdf_path, output_dir, deskew=True, use_tf=False, save_cache=False):
    """
    Converts a PDF to MusicXML and MuseScore format using homr.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the output files.
        deskew (bool): Whether to perform deskewing (default: True).
        use_tf (bool): Use Tensorflow for model inference (default: False).
        save_cache (bool): Save model predictions for future use (default: False).
    """

    output_dir = os.path.join(os.path.abspath(output_dir), os.path.splitext(os.path.basename(pdf_path))[0])
    image_dir = os.path.join(output_dir, "images")
    musicxml_dir = os.path.join(output_dir, "musicxml")


    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir, exist_ok=True)
    if not os.path.exists(musicxml_dir):
        os.makedirs(musicxml_dir, exist_ok=True)

    # Convert PDF to PNG images
    pdf_to_png(pdf_path, image_dir)

    # Run homr on each PNG image
    original_dir = os.getcwd()
    os.chdir(output_dir)
    for filename in os.listdir(image_dir):
        if filename.endswith(".png"):
            image_path = os.path.join(image_dir, filename)
            try:
                command = ["homr", image_path]
                if not deskew:
                    command.append("--without-deskew")
                if use_tf:
                    command.append("--use-tf")
                if save_cache:
                    command.append("--save-cache")
                result = subprocess.run(
                    command,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                print(result.stdout)  # Print the output of homr
                print(f"Successfully processed {filename}")
                # Move the musicxml file to the musicxml directory
                for file in os.listdir("."):
                    if file.endswith(".musicxml"):
                        shutil.move(file, musicxml_dir)

            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}: {e.stderr}")
    os.chdir(original_dir)

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
    return musescore_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF sheet music to MusicXML and MuseScore format.")
    parser.add_argument("pdf_path", nargs='?', help="Path to the input PDF file.")
    parser.add_argument("output_dir", nargs='?', help="Path to the output directory.")
    parser.add_argument("--use-tf", action="store_true", help="Use Tensorflow for model inference. Default is to use Onnxruntime. (default: False)")
    parser.add_argument("--save-cache", action="store_true", help="Save the model predictions and the next time won't need to predict again. (default: False)")
    parser.add_argument("-d", "--without-deskew", dest="deskew", action="store_false", help="Disable the deskewing step if you are sure the image has no skew. (default: False)")
    parser.add_argument("--gradio", action="store_true", help="Launch Gradio UI.")
    parser.set_defaults(deskew=True)

    args = parser.parse_args()

    if args.gradio:
        print("Launching Gradio UI")
        subprocess.run(["python", "gradio_app.py"])
    elif args.pdf_path and args.output_dir:
        main(args.pdf_path, args.output_dir, args.deskew, args.use_tf, args.save_cache)
    else:
        parser.print_help()
        sys.exit(1)
