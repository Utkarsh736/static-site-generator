import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = (
            "\n"
            "This is **bolded** paragraph\n"
            "\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line\n"
            "\n"
            "- This is a list\n"
            "- with items\n"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = (
            "\n"
            "# This is a heading\n"
            "\n"
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n"
            "\n"
            "- This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item\n"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(
            blocks[1],
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
        )
        self.assertEqual(
            blocks[2],
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = "\n\n\nBlock one\n\n\nBlock two\n\n\n\nBlock three\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one", "Block two", "Block three"])

    def test_markdown_to_blocks_whitespace_stripping(self):
        md = "\n   Leading and trailing spaces   \n\n\tTabs too\t\n\nNormal text\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Leading and trailing spaces", "Tabs too", "Normal text"]
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just one line of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one line of text"])

    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n  \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_preserves_internal_newlines(self):
        md = "\nLine 1\nLine 2\nLine 3\n\nDifferent block\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1\nLine 2\nLine 3", "Different block"])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h2(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_invalid_no_space(self):
        block = "#No space after hash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_invalid_too_many_hashes(self):
        block = "####### Seven hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_language(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiple_lines(self):
        block = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_invalid_missing_space(self):
        block = ">No space after"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_invalid_not_all_lines(self):
        block = "> Line 1\nLine 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_dash(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_asterisk(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        block = "- Single item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid_no_space(self):
        block = "-No space\n-After dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_invalid_not_all_lines(self):
        block = "- Item 1\nNot an item\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        block = "1. Only one"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_wrong_start(self):
        block = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_not_sequential(self):
        block = "1. First\n3. Third\n4. Fourth"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_no_space(self):
        block = "1.No space\n2.After period"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_plain_text(self):
        block = "This is just a regular paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "Line 1\nLine 2\nLine 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_inline_markdown(self):
        block = "This has **bold** and *italic* text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = (
            "\n"
            "This is **bolded** paragraph\n"
            "text in a p\n"
            "tag here\n"
            "\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "\n"
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "\n```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_heading_with_inline(self):
        md = "## Heading with **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>Heading with <b>bold</b> text</h2></div>")

    def test_quote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

    def test_unordered_list(self):
        md = "\n- Item 1\n- Item 2\n- Item 3\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "\n1. First\n2. Second\n3. Third\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_all_block_types(self):
        md = (
            "\n"
            "# Heading\n"
            "\n"
            "Paragraph text here.\n"
            "\n"
            "- List item\n"
            "- Another item\n"
            "\n"
            "> A quote\n"
            "\n"
            "```\n"
            "code block\n"
            "```\n"
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn("<p>Paragraph text here.</p>", html)
        self.assertIn("<ul><li>List item</li><li>Another item</li></ul>", html)
        self.assertIn("<blockquote>A quote</blockquote>", html)
        self.assertIn("<pre><code>code block\n</code></pre>", html)


if __name__ == "__main__":
    unittest.main()

