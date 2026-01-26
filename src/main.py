import os
import shutil
import sys

from block_markdown import markdown_to_html_node, extract_title


def copy_static_to_public(src_dir="static", dest_dir="docs"):
    """
    Recursively copy all contents from src_dir to dest_dir.
    Deletes dest_dir first to ensure a clean copy.
    """
    if os.path.exists(dest_dir):
        print(f"Deleting {dest_dir} directory...")
        shutil.rmtree(dest_dir)
    
    print(f"Creating {dest_dir} directory...")
    os.mkdir(dest_dir)
    
    _copy_directory_contents(src_dir, dest_dir)


def _copy_directory_contents(src, dest):
    """
    Helper function to recursively copy directory contents.
    """
    if not os.path.exists(src):
        raise ValueError(f"Source directory does not exist: {src}")
    
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_directory_contents(src_path, dest_path)


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from markdown using a template.
    
    Args:
        from_path: Path to markdown file
        template_path: Path to HTML template file
        dest_path: Path to write generated HTML file
        basepath: Base path for URLs (e.g., "/" or "/repo-name/")
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Replace root-relative URLs with basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the generated HTML to destination
    with open(dest_path, 'w') as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages from all markdown files in a directory tree.
    
    Args:
        dir_path_content: Root content directory to crawl
        template_path: Path to HTML template file
        dest_dir_path: Root destination directory for generated HTML
        basepath: Base path for URLs (e.g., "/" or "/repo-name/")
    """
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Content directory does not exist: {dir_path_content}")
    
    items = os.listdir(dir_path_content)
    
    for item in items:
        src_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(src_path):
            if item.endswith('.md'):
                html_filename = item.replace('.md', '.html')
                dest_path = os.path.join(dest_dir_path, html_filename)
                generate_page(src_path, template_path, dest_path, basepath)
        else:
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, new_dest_dir, basepath)


def main():
    # Get basepath from command line argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"Using basepath: {basepath}")
    print("Starting static site generator...\n")
    
    # Copy static files to docs
    copy_static_to_public(src_dir="static", dest_dir="docs")
    
    print("\n" + "="*50)
    print("Generating pages...\n")
    
    # Generate all pages recursively
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
    print("\n" + "="*50)
    print("Static site generation complete!")


if __name__ == "__main__":
    main()

