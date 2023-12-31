import os
import markdown2

def convert_md_to_html(md_file_path, output_file_path):
    """
    Convert a Markdown file to HTML format.

    Args:
    - md_file_path (str): Path to the Markdown file.
    - output_file_path (str): Path to output the converted HTML file.
    """
    with open(md_file_path, 'r') as md_file:
        markdown_text = md_file.read()

    extras = ["tables", "fenced-code-blocks", "header-ids", "smarty-pants", "toc"]
    html = markdown2.markdown(markdown_text, extras=extras)

    with open(output_file_path, 'w') as html_file:
        html_file.write(html)

def convert_directory(input_dir, output_dir):
    """
    Convert all Markdown files in a directory (and its subdirectories) to HTML format.

    Args:
    - input_dir (str): Path to the directory containing Markdown files.
    - output_dir (str): Path to the directory where the converted HTML files will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_file_dir = os.path.join(output_dir, relative_path)
                output_file_path = os.path.join(output_file_dir, os.path.splitext(file)[0] + '.html')
                
                if not os.path.exists(output_file_dir):
                    os.makedirs(output_file_dir)

                convert_md_to_html(md_file_path, output_file_path)
                print(f"Converted '{md_file_path}' to '{output_file_path}'")
