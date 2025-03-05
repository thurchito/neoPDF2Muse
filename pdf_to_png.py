import os
import sys
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import cv2
from collections import Counter

def calculate_thickness_spacing(rle, most_common):
    # Placeholder implementation
    return 5, 10

def most_common_bw_pattern(col, most_common):
    # Placeholder implementation
    return None

def hv_rle(img):
    # Placeholder implementation
    return [], []

def get_most_common(rle):
    # Placeholder implementation
    return None

def remove_staff_lines(rle, vals, thickness, shape):
    # Placeholder implementation
    return np.ones(shape, dtype=np.uint8)

def get_line_indices(hist):
     #simple implementation
    line_indices = []
    for i in range(1, len(hist) - 1):
        if hist[i] > hist[i - 1] and hist[i] > hist[i + 1]:
            line_indices.append(i)
    return line_indices
    
def histogram(img, threshold):
    # Create a binary histogram
    binary_img = (img < threshold).astype(np.uint8)
    return np.sum(binary_img, axis=1)

def pdf_to_png(pdf_path, output_dir):
    """
    Converts each page of a PDF to a PNG image and segments staff lines.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the PNG images.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        images = convert_from_path(pdf_path)
        for page_num, image in enumerate(images):
            img = np.array(image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # Staff line segmentation logic
            rle, vals = hv_rle(thresh)
            most_common = get_most_common(rle)
            thickness, spacing = calculate_thickness_spacing(rle, most_common)
            no_staff_img = remove_staff_lines(rle, vals, thickness, thresh.shape)

            line_indices = get_line_indices(histogram(thresh, 0.8))

            if len(line_indices) < 10:
                # Not enough staff lines detected, save the whole page
                image.save(os.path.join(output_dir, f"page_{page_num}.png"), "PNG")
                continue

            lines = []
            for index in line_indices:
                line = ((0, index), (thresh.shape[1] - 1, index))
                lines.append(line)

            end_of_staff = []
            for index, line in enumerate(lines):
                if index > 0 and (line[0][1] - end_of_staff[-1][1] < 4 * spacing):
                    pass  # Skip lines that are too close together
                else:
                    p1, p2 = line
                    x0, y0 = p1
                    x1, y1 = p2
                    end_of_staff.append((x0, y0, x1, y1))

            box_centers = []
            spacing_between_staff_blocks = []
            for i in range(len(end_of_staff) - 1):
                spacing_between_staff_blocks.append(
                    end_of_staff[i + 1][1] - end_of_staff[i][1]
                )
                if i % 2 == 0:
                    offset = (end_of_staff[i + 1][1] - end_of_staff[i][1]) // 2
                    center = end_of_staff[i][1] + offset
                    box_centers.append((center, offset))

            max_staff_dist = np.max(spacing_between_staff_blocks)
            max_margin = max_staff_dist // 2
            margin = max_staff_dist // 10

            for index, (center, offset) in enumerate(box_centers):
                y0 = int(center) - max_margin - offset + margin
                y1 = int(center) + max_margin + offset - margin
                # Ensure y0 and y1 are within the image bounds
                y0 = max(0, y0)
                y1 = min(img.shape[0], y1)
                
                staff_region = img[y0:y1, 0:img.shape[1]]
                staff_image = Image.fromarray(staff_region)
                staff_image.save(os.path.join(output_dir, f"page_{page_num}_staff_{index}.png"), "PNG")

            print(f"PDF to PNG conversion and staff line segmentation complete for page {page_num}!")

    except Exception as e:
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_png.py <pdf_path> <output_dir>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]

    pdf_to_png(pdf_path, output_dir)
