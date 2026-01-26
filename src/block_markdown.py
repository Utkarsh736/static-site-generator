from enum import Enum
import re

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    Returns a BlockType enum value.
    """
    lines = block.split("\n")
    
    # Check for heading (1-6 # followed by space)
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with "> ")
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- " or "* ")
    if all(line.startswith("- ") or line.startswith("* ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with "1. ", "2. ", etc.)
    is_ordered_list = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered_list = False
            break
    
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    """
    Split a markdown document into block strings.
    Blocks are separated by blank lines (double newlines).
    Returns a list of block strings with whitespace stripped.
    """
    blocks = markdown.split("\n\n")
    
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    
    return filtered_blocks


def text_to_children(text):
    """
    Convert inline markdown text to a list of HTMLNode children.
    This handles bold, italic, code, links, and images.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    lines = block.split("\n")
    paragraph_text = " ".join(lines)
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    # Count the number of # characters
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")

    # Remove the # characters and leading space
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    # Remove the opening and closing ```
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")

    # Extract code content (remove ``` from start and end)
    code_text = block[4:-3]

    # Code blocks don't parse inline markdown
    code_node = LeafNode("code", code_text)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split("\n")

    # Remove "> " from the start of each line
    new_lines = []
    for line in lines:
        if not line.startswith("> "):
            raise ValueError("Invalid quote block")
        new_lines.append(line[2:])

    # Join lines and parse inline markdown
    quote_text = "\n".join(new_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []

    for line in lines:
        # Remove "- " or "* " from the start
        if line.startswith("- "):
            text = line[2:]
        elif line.startswith("* "):
            text = line[2:]
        else:
            raise ValueError("Invalid unordered list item")

        children = text_to_children(text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []

    for i, line in enumerate(lines, start=1):
        # Check that it starts with "i. "
        if not line.startswith(f"{i}. "):
            raise ValueError("Invalid ordered list item")

        text = line[len(f"{i}. "):]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document to an HTMLNode.
    Returns a parent div containing all block-level elements.
    """
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode("div", children)

def extract_title(markdown):
    """
    Extract the h1 header from markdown.
    Returns the title text without the # prefix.
    Raises ValueError if no h1 header is found.
    """
    lines = markdown.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            # Remove the "# " prefix and return
            return line[2:].strip()

    raise ValueError("No h1 header found in markdown")
