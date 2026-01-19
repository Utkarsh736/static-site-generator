import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        # Only split TEXT type nodes, pass others through unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        sections = old_node.text.split(delimiter)
        
        # Check for unclosed delimiter (odd number of sections means unclosed)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown: unclosed delimiter '{delimiter}'")
        
        # Process sections: alternating between TEXT and the specified text_type
        for i, section in enumerate(sections):
            if section == "":
                continue
            
            # Even indices (0, 2, 4...) are plain text
            # Odd indices (1, 3, 5...) are delimited text
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))
    
    return new_nodes

def extract_markdown_images(text):
    """
    Extract markdown images from text.
    Returns list of tuples: (alt_text, url)
    Pattern: ![alt text](url)
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text (excluding images).
    Returns list of tuples: (anchor_text, url)
    Pattern: [text](url) but NOT ![text](url)
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    """
    Split TEXT nodes containing markdown images into separate nodes.
    Images become IMAGE type nodes, surrounding text stays TEXT type.
    """
    new_nodes = []

    for old_node in old_nodes:
        # Only split TEXT type nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Extract all images from this node
        images = extract_markdown_images(old_node.text)

        # If no images, keep the node as-is
        if not images:
            new_nodes.append(old_node)
            continue

        # Process the text, splitting by each image
        remaining_text = old_node.text

        for alt_text, url in images:
            # Construct the full markdown syntax to split on
            markdown_image = f"![{alt_text}]({url})"

            # Split on this image (max 1 split to handle same image multiple times)
            parts = remaining_text.split(markdown_image, 1)

            if len(parts) != 2:
                raise ValueError(f"Image markdown '{markdown_image}' not found in text")

            # Add the text before the image (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Continue with the remaining text
            remaining_text = parts[1]

        # Add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TEXT nodes containing markdown links into separate nodes.
    Links become LINK type nodes, surrounding text stays TEXT type.
    """
    new_nodes = []

    for old_node in old_nodes:
        # Only split TEXT type nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Extract all links from this node
        links = extract_markdown_links(old_node.text)

        # If no links, keep the node as-is
        if not links:
            new_nodes.append(old_node)
            continue

        # Process the text, splitting by each link
        remaining_text = old_node.text

        for anchor_text, url in links:
            # Construct the full markdown syntax to split on
            markdown_link = f"[{anchor_text}]({url})"

            # Split on this link (max 1 split to handle same link multiple times)
            parts = remaining_text.split(markdown_link, 1)

            if len(parts) != 2:
                raise ValueError(f"Link markdown '{markdown_link}' not found in text")

            # Add the text before the link (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            # Continue with the remaining text
            remaining_text = parts[1]

        # Add any remaining text after the last link
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    """
    Convert raw markdown text to a list of TextNode objects.
    Handles all inline markdown: images, links, bold, italic, and code.
    """
    # Start with a single TEXT node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process in order: images and links first, then delimiters
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes

