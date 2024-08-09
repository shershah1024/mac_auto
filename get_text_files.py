import os
from fpdf import FPDF
import string

def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in filename if c in valid_chars)
    return cleaned_filename

def convert_ts_files_to_pdf(source_folder, target_folder):
    os.makedirs(target_folder, exist_ok=True)

    for root, dirs, files in os.walk(source_folder):
        # Skip node_modules directories
        if 'node_modules' in dirs:
            dirs.remove('node_modules')

        for file in files:
            if file.endswith(('.ts', '.tsx')):
                try:
                    source_path = os.path.join(root, file)
                    
                    # Skip files in node_modules directories
                    if 'node_modules' in source_path:
                        continue

                    relative_path = os.path.relpath(source_path, source_folder)
                    # Create a unique filename by replacing path separators
                    unique_filename = sanitize_filename(relative_path.replace(os.sep, '_') + '.pdf')
                    target_path = os.path.join(target_folder, unique_filename)

                    # Create a PDF document
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)

                    # Read the source file and add its content to the PDF
                    with open(source_path, 'r', encoding='utf8') as f:
                        for line in f:
                            pdf.cell(200, 10, txt=line, ln=True)

                    # Save the PDF to the target path
                    pdf.output(target_path)
                    print(f"Converted: {source_path} -> {target_path}")
                except Exception as e:
                    print(f"Failed to convert {source_path}: {e}")


convert_ts_files_to_pdf(source_folder="/Users/shahir/agents-playground/src", target_folder="/Users/shahir/Downloads/target_folder")