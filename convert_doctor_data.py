"""
Doctor Preferences Markdown to HTML Converter

This script converts markdown files in the doctor_data folder to HTML files
that can be loaded by the doctor preferences web application.

Usage:
    python convert_doctor_data.py

The script will:
1. Read all .md files from the doctor_data folder
2. Convert them to HTML
3. Save them to the doctor_html folder
4. Generate a doctors_list.js file with all available doctors
"""

import os
import re
from pathlib import Path


# ===== CONFIGURATION =====
# Set to None to use the script's location, or specify a path
# Example: WORK_DIRECTORY = r"D:\Nobue"
WORK_DIRECTORY = None  # Change this to your shared drive path if needed
# ==========================


def markdown_to_html(markdown_text):
    """
    Convert markdown to HTML.
    Supports: headers, bold, italic, lists, paragraphs
    """
    html = markdown_text

    # Convert headers (## Header -> <h2>Header</h2>)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)

    # Convert bold (**text** -> <strong>text</strong>)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)

    # Convert italic (*text* -> <em>text</em>)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

    # Convert unordered lists (- item -> <li>item</li>)
    lines = html.split("\n")
    in_list = False
    result_lines = []

    for line in lines:
        if line.strip().startswith("- "):
            if not in_list:
                result_lines.append("<ul>")
                in_list = True
            item = line.strip()[2:]  # Remove '- '
            result_lines.append(f"<li>{item}</li>")
        else:
            if in_list:
                result_lines.append("</ul>")
                in_list = False
            result_lines.append(line)

    if in_list:
        result_lines.append("</ul>")

    html = "\n".join(result_lines)

    # Convert paragraphs (text not in other tags -> <p>text</p>)
    lines = html.split("\n")
    result_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped and not any(
            stripped.startswith(tag)
            for tag in ["<h1>", "<h2>", "<h3>", "<ul>", "</ul>", "<li>"]
        ):
            result_lines.append(f"<p>{stripped}</p>")
        else:
            result_lines.append(line)

    return "\n".join(result_lines)


def get_doctor_name_from_filename(filename):
    """
    Convert filename to doctor display name.
    Example: Dr_Smith.md -> Dr. Smith
    """
    name = Path(filename).stem  # Remove .md extension
    name = name.replace("_", " ")  # Replace underscores with spaces
    return name


def convert_all_doctors():
    """
    Convert all markdown files in doctor_data folder to HTML.
    """
    # Change to work directory if specified
    if WORK_DIRECTORY:
        if not os.path.exists(WORK_DIRECTORY):
            print(f"Error: Work directory not found: {WORK_DIRECTORY}")
            print("Please check the path and try again.")
            return
        os.chdir(WORK_DIRECTORY)
        print(f"Working in: {WORK_DIRECTORY}\n")

    # Create folders if they don't exist
    data_folder = Path("doctor_data")
    html_folder = Path("doctor_html")
    html_folder.mkdir(exist_ok=True)

    if not data_folder.exists():
        print(f"Error: {data_folder} folder not found!")
        print("Please create the folder and add markdown files for each doctor.")
        return

    # Get all markdown files
    md_files = list(data_folder.glob("*.md"))

    if not md_files:
        print(f"No markdown files found in {data_folder}")
        return

    doctor_list = []

    # Convert each markdown file
    for md_file in md_files:
        print(f"Converting {md_file.name}...")

        # Read markdown content
        with open(md_file, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Convert to HTML
        html_content = markdown_to_html(markdown_content)

        # Get doctor name
        doctor_name = get_doctor_name_from_filename(md_file.name)
        doctor_list.append({"name": doctor_name, "file": md_file.stem + ".html"})

        # Save HTML file
        html_file = html_folder / (md_file.stem + ".html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"  ✓ Created {html_file}")

    # Generate JavaScript file with doctor list
    js_content = "// Auto-generated list of doctors\n"
    js_content += "const doctorsList = [\n"

    for doctor in sorted(doctor_list, key=lambda x: x["name"]):
        js_content += f"    {{ name: '{doctor['name']}', file: '{doctor['file']}' }},\n"

    js_content += "];\n"

    js_file = html_folder / "doctors_list.js"
    with open(js_file, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"\n✓ Created {js_file}")
    print(f"\nConversion complete! Processed {len(doctor_list)} doctors.")
    print(f"HTML files are in the '{html_folder}' folder.")


if __name__ == "__main__":
    print("Doctor Preferences Markdown to HTML Converter")
    print("=" * 50)
    convert_all_doctors()
