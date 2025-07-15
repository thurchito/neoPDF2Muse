import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import subprocess
import platform
import ms3
from shutil import which

MXML_NS = "http://www.musicxml.org/ns/musicxml"
ET.register_namespace("", MXML_NS)

def join_musicxml_files(input_dir, output_file):
    files = sorted(f for f in os.listdir(input_dir) if f.lower().endswith(".musicxml"))
    if not files:
        raise ValueError("No .musicxml files found.")

    # Parse the first file and get its tree/root
    first_path = os.path.join(input_dir, files[0])
    tree = ET.parse(first_path)
    root = tree.getroot()

    # Grab the part-list from the first file
    part_list = root.find(f"{{{MXML_NS}}}part-list")
    parts      = {p.get("id"): p for p in root.findall(f"{{{MXML_NS}}}part")}

    # Now loop over the rest
    for fn in files[1:]:
        path = os.path.join(input_dir, fn)
        sub_tree = ET.parse(path)
        sub_root = sub_tree.getroot()

        # Merge score-part definitions
        for sp in sub_root.findall(f".//{{{MXML_NS}}}score-part"):
            pid = sp.get("id")
            # only add if not already in master part-list
            if part_list.find(f"{{{MXML_NS}}}score-part[@id='{pid}']") is None:
                part_list.append(sp)

        # Merge the actual <part> elements
        for part in sub_root.findall(f"{{{MXML_NS}}}part"):
            parts[part.get("id")] = part

    # Remove all old <part> nodes then re-append in sorted order
    for old in list(root.findall(f"{{{MXML_NS}}}part")):
        root.remove(old)
    for pid in sorted(parts):
        root.append(parts[pid])

    # Write it back out
    tree.write(output_file,
               encoding="UTF-8",
               xml_declaration=True)
    print(f"Written combined MusicXML to {output_file}")

def convert_to_musescore_format(input_file, output_file, format="mscx"):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file does not exist: {input_file}")

    # Load MusicXML into ms3 Score object
    score = ms3.Score(input_file)

    # Save as .mscz
    score.save(output_file)
    print(f"Conversion successful! Output saved to: {output_file}")

if __name__ == '__main__':
    # Example usage
    # Create a dummy directory with dummy musicxml files
    os.makedirs("test_musicxml", exist_ok=True)
    with open("test_musicxml/page1.musicxml", "w") as f:
        f.write("<score-partwise version='3.1'><part id='P1'><measure number='1'><note><pitch><step>C</step><octave>4</octave></pitch><duration>4</duration></note></measure></score-partwise>")
    with open("test_musicxml/page2.musicxml", "w") as f:
        f.write("<score-partwise version='3.1'><part id='P1'><measure number='2'><note><pitch><step>D</step><octave>4</octave></pitch><duration>4</duration></note></measure></score-partwise>")

    join_musicxml_files("test_musicxml", "combined.musicxml")
    convert_to_musescore_format("combined.musicxml", "combined.mscx")
