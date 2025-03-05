import os
import sys
from PIL import Image

def pdf_to_png(pdf_path, output_dir):
    """
    Converts each page of a PDF to a PNG image using PIL.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the PNG images.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Open the PDF with Pillow
        img = Image.open(pdf_path)

        # Iterate over all pages
        for i in range(img.n_frames):
            img.seek(i)
            img.save(os.path.join(output_dir, f"page_{i}.png"), "PNG")

        print("PDF to PNG conversion complete!")

    except Exception as e:
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_png.py <pdf_path> <output_dir>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]

    pdf_to_png(pdf_path, output_dir)
