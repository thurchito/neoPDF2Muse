import gradio as gr
import argparse
from main import main  # Import the main function from main.py

def convert_pdf_to_musicxml(pdf_file, output_dir, deskew):
    """
    Converts a PDF to MusicXML and MuseScore format using oemer.

    Args:
        pdf_file (file): The uploaded PDF file.
        output_dir (str): Directory to save the output files.
        deskew (bool): Whether to perform deskewing.
    Returns:
        tuple: A tuple containing the status message and the path to the generated .mscx file.
    """
    try:
        # Call the existing main function
        musescore_file = main(pdf_file.name, output_dir, deskew)
        return "PDF to MusicXML and MuseScore conversion complete!", musescore_file
    except Exception as e:
        return f"Error processing PDF: {e}", None


if __name__ == "__main__":
    with gr.Blocks() as interface:
        pdf_input = gr.File(label="Upload PDF")
        output_dir_input = gr.Textbox(label="Output Directory", value="output")
        deskew_checkbox = gr.Checkbox(label="Enable Deskewing", value=False)
        status_output = gr.Textbox(label="Status")
        mscx_output = gr.File(label="Download MuseScore File")
        convert_button = gr.Button("Convert")

        convert_button.click(
            convert_pdf_to_musicxml,
            inputs=[pdf_input, output_dir_input, deskew_checkbox],
            outputs=[status_output, mscx_output],
        )

    interface.launch(share=True)
