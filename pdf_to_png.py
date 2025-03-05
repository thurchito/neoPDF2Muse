import os
import sys
from pdf2image import convert_from_path

def pdf_to_png(pdf_path, output_dir):
    """
    Converts each page of a PDF to a PNG image using pdf2image.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the PNG images.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image.save(os.path.join(output_dir, f"page_{i}.png"), "PNG")
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
