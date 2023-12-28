import argparse
import os
from markdown_to_confluence.converter import convert_directory
from markdown_to_confluence.sync import sync_to_confluence

def main():
    """
    CLI for Markdown to Confluence conversion and synchronization tool.
    """
    parser = argparse.ArgumentParser(description="Markdown to Confluence Tool")
    parser.add_argument("--convert", action="store_true", help="Convert Markdown to HTML")
    parser.add_argument("--sync", action="store_true", help="Sync HTML files to Confluence")
    parser.add_argument("--input-dir", help="Input directory for Markdown files")
    parser.add_argument("--output-dir", help="Output directory for HTML files")
    parser.add_argument("--space-key", help="Confluence Space Key", default=os.environ.get('CONFLUENCE_SPACE_KEY'))
    parser.add_argument("--parent-id", type=int, help="Parent Page ID in Confluence", default=os.environ.get('CONFLUENCE_PARENT_ID'))
    parser.add_argument("--base-url", help="Confluence Base URL", default=os.environ.get('CONFLUENCE_BASE_URL'))
    parser.add_argument("--username", help="Confluence Username", default=os.environ.get('CONFLUENCE_USERNAME'))
    parser.add_argument("--api-token", help="Confluence API Token", default=os.environ.get('CONFLUENCE_API_TOKEN'))

    args = parser.parse_args()

    # Handle Markdown to HTML conversion
    if args.convert and args.input_dir and args.output_dir:
        convert_directory(args.input_dir, args.output_dir)

    # Handle synchronization with Confluence
    if args.sync:
        if args.output_dir and all([args.space_key, args.base_url, args.username, args.api_token]):
            sync_to_confluence(args.output_dir, args.parent_id, args.space_key, args.base_url, args.username, args.api_token)
        else:
            print("Required arguments for synchronization are missing.")
            parser.print_help()

if __name__ == "__main__":
    main()
