import os
import sys
from PyPDF2 import PdfReader
from PIL import Image

def pdf_to_png(pdf_path, output_dir):
    """
    Converts each page of a PDF to a PNG image.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the PNG images.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        reader = PdfReader(pdf_path)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            try:
                image = page.images[0]
                with open(os.path.join(output_dir, f"page_{page_num}.png"), "wb") as f:
                    f.write(image.data)
            except IndexError:
                print(f"No image found on page {page_num + 1}")
    except Exception as e:
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_png.py <pdf_path> <output_dir>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]

    pdf_to_png(pdf_path, output_dir)
    print("PDF to PNG conversion complete!")
