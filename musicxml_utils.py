import os
import zipfile
import xml.etree.ElementTree as ET
import subprocess
from msczyx import Score

def convert_to_musescore_format(input_file, output_file, format="mscx"):
    """
    Converts a MusicXML file to MuseScore format (.mscx or .mscz) using msczyx.

    Args:
        input_file (str): Path to the input MusicXML file.
        output_file (str): Path to the output MuseScore file (.mscx or .mscz).
        format (str): Output format: 'mscx' or 'mscz'.
    """

    try:
        print("Reading MusicXML...")
        score = Score.from_musicxml(input_file)

        if format == "mscx":
            score.write_mscx(output_file)
        elif format == "mscz":
            score.write_mscz(output_file)
        else:
            print("Unsupported format. Use 'mscx' or 'mscz'.")
            return

        print(f"Successfully converted {input_file} to {output_file}")

    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"Error converting to MuseScore format: {e}")

def join_musicxml_files(input_dir, output_file):
    """
    Joins multiple MusicXML files into a single MusicXML file.

    Args:
        input_dir (str): Directory containing the MusicXML files.
        output_file (str): Path to the output MusicXML file.
    """

    # Get a list of all MusicXML files in the input directory
    musicxml_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".musicxml")])

    if not musicxml_files:
        print("No MusicXML files found in the input directory.")
        return

    # Parse the first MusicXML file to get the root element
    first_musicxml_file = os.path.join(input_dir, musicxml_files[0])
    tree = ET.parse(first_musicxml_file)
    root = tree.getroot()
    ns = {'ns': 'http://www.musicxml.org/ns/musicxml'}
    part_list = root.find("ns:part-list", ns)
    parts = root.findall("ns:part", ns) 

    # Find the part list and part elements
    part_list = root.find("part-list")
    parts = root.findall("part")

    # Iterate over the remaining MusicXML files and append their part elements
    for musicxml_file in musicxml_files[1:]:
        musicxml_path = os.path.join(input_dir, musicxml_file)
        tree = ET.parse(musicxml_path)
        new_root = tree.getroot()
        new_parts = new_root.findall("part")
        for new_part in new_parts:
            parts.append(new_part)

    # Remove existing parts and append the combined parts
    for part in root.findall("part"):
        root.remove(part)
    for part in parts:
        root.append(part)

    # Write the combined MusicXML to the output file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True, default_namespace=None)

    print(f"Successfully joined MusicXML files into {output_file}")


def convert_to_musescore_format(input_file, output_file, format="mscx"):
    """
    Converts a MusicXML file to MuseScore format (.mscx).

    Args:
        input_file (str): Path to the input MusicXML file.
        output_file (str): Path to the output MuseScore file.
    """

    if format != "mscx":
        print("Only .mscx conversion is supported at this time.")
        return

    try:
        # Parse the MusicXML file
        tree = ET.parse(input_file)
        root = tree.getroot()
        ns = {'ns': 'http://www.musicxml.org/ns/musicxml'}
        part_list = root.find("ns:part-list", ns)
        parts = root.findall("ns:part", ns)

        # Create the root element for the MuseScore file
        musescore = ET.Element("museScore", {"version": "4.0"})
        # Create the score element
        score = ET.SubElement(musescore, "Score")

        # Copy the division from the MusicXML file
        division = root.find("division")
        if division is not None:
            score.append(division)

        # Copy the parts from the MusicXML file
        part_list = root.find("part-list")
        if part_list is not None:
            score.append(part_list)

        parts = root.findall("part")
        for part in parts:
            score.append(part)

        # Create the ElementTree and write to the output file
        mscx_tree = ET.ElementTree(musescore)
        mscx_tree.write(output_file, encoding="UTF-8", xml_declaration=True, default_namespace=None)

        print(f"Successfully converted {input_file} to {output_file}")

    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"Error converting file: {e}")

if __name__ == '__main__':
    # Example usage
    # Create a dummy directory with dummy musicxml files
    os.makedirs("test_musicxml", exist_ok=True)
    with open("test_musicxml/page1.musicxml", "w") as f:
        f.write("<score-partwise version='3.1'><part id='P1'><measure number='1'><note><pitch><step>C</step><octave>4</octave></pitch><duration>4</duration></note></measure></part></score>")
    with open("test_musicxml/page2.musicxml", "w") as f:
        f.write("<score-partwise version='3.1'><part id='P1'><measure number='2'><note><pitch><step>D</step><octave>4</octave></pitch><duration>4</duration></note></measure></part></score>")

    join_musicxml_files("test_musicxml", "combined.musicxml")
    convert_to_musescore_format("combined.musicxml", "combined.mscx")