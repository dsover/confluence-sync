import os
from .uploader import add_or_update_page

def sync_to_confluence(output_dir, root_parent_id, space_key, base_url, username, api_token):
    """
    Synchronize the converted HTML files to Confluence with a structure 
    mirroring the directory layout.

    Args:
    - output_dir (str): The directory containing the converted HTML files.
    - root_parent_id (int): The ID of the root parent page in Confluence.
    - space_key (str): The key of the space in Confluence.
    - base_url (str): The base URL of the Confluence instance.
    - username (str): Confluence username.
    - api_token (str): Confluence API token.
    """
    directory_page_ids = {os.path.normpath(output_dir): root_parent_id}

    for root, dirs, files in os.walk(output_dir, topdown=True):
        norm_root = os.path.normpath(root)
        parent_id = directory_page_ids[norm_root]

        # Handle directories and subdirectories
        for dir_name in dirs:
            dir_path = os.path.normpath(os.path.join(root, dir_name))
            # Check for README.md in the directory
            readme_path = os.path.join(dir_path, "README.html")
            if os.path.exists(readme_path):
                with open(readme_path, 'r') as file:
                    content = file.read()
                page_id = add_or_update_page(dir_name, content, space_key, parent_id, base_url, username, api_token)
            else:
                # Create stub with links to pages in the directory
                links = [f"[{os.path.splitext(file)[0]}|{os.path.splitext(file)[0].replace(' ', '+')}]" for file in files if file.endswith(".html")]
                links_content = '\n'.join(links)
                stub_content = f"<h2>Contents of {dir_name}</h2>\n{links_content}"
                page_id = add_or_update_page(dir_name, stub_content, space_key, parent_id, base_url, username, api_token)
            directory_page_ids[dir_path] = page_id

        # Process Markdown files in the current directory
        for file_name in files:
            if file_name.endswith(".html") and file_name != "README.md":
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()
                title = os.path.splitext(file_name)[0]
                add_or_update_page(title, content, space_key, directory_page_ids[norm_root], base_url, username, api_token)

