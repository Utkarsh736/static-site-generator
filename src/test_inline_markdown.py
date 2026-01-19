import unittest
from textnode import TextNode, TextType

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_all_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text with no formatting"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text with no formatting", TextType.TEXT)]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_italic_only(self):
        text = "This is *italic* text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_code_only(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_image_only(self):
        text = "Check out this ![image](https://example.com/pic.png) please"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/pic.png"),
            TextNode(" please", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_link_only(self):
        text = "Visit [my site](https://example.com) today"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("my site", TextType.LINK, "https://example.com"),
            TextNode(" today", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_multiple_same_type(self):
        text = "**bold1** and **bold2** with `code1` and `code2`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_mixed_delimiters(self):
        text = "**bold** *italic* `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)
    
    def test_text_to_textnodes_complex_nested(self):
        text = "Start **bold with *italic* inside** end"
        nodes = text_to_textnodes(text)
        # Bold gets processed first, capturing everything between **
        # The * characters inside bold become literal text
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold with *italic* inside", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_image_and_link(self):
        text = "![img](pic.png) and [link](url.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "pic.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        # Empty string results in empty list after filtering
        expected = []
        self.assertListEqual(expected, nodes)    


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_single(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_bold_single(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_italic_single(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_multiple_delimiters(self):
        node = TextNode("Code `one` and `two` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Code ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_no_delimiter(self):
        node = TextNode("Plain text with no formatting", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("Plain text with no formatting", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_delimiter_at_start(self):
        node = TextNode("**Bold** at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_delimiter_at_end(self):
        node = TextNode("End with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_entire_text_delimited(self):
        node = TextNode("`all code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("all code", TextType.CODE)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("Already bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("First `code` here", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Second `code` here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_unclosed_delimiter_raises_error(self):
        node = TextNode("Unclosed `delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unclosed", str(context.exception).lower())
    
    def test_split_consecutive_delimiters(self):
        node = TextNode("Text **bold****another** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("another", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_images_none(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_empty_alt(self):
        text = "Image with empty alt ![](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.png")], matches)
    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_links_none(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_ignores_images(self):
        text = "Link [here](https://example.com) and image ![alt](https://example.com/img.png)"
        matches = extract_markdown_links(text)
        # Should only get the link, not the image
        self.assertListEqual([("here", "https://example.com")], matches)
    
    def test_extract_both_images_and_links(self):
        text = "Check ![image](https://img.com/pic.jpg) and [link](https://site.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("image", "https://img.com/pic.jpg")], images)
        self.assertListEqual([("link", "https://site.com")], links)
    
    def test_extract_markdown_links_with_special_chars(self):
        text = "[Google Search](https://www.google.com/search?q=python&lang=en)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("Google Search", "https://www.google.com/search?q=python&lang=en")],
            matches
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_single(self):
        node = TextNode(
            "Text with ![one image](https://example.com/img.png) here",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("one image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_no_images(self):
        node = TextNode("Plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Plain text with no images", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_at_start(self):
        node = TextNode(
            "![start image](https://example.com/start.png) followed by text",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "https://example.com/start.png"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_at_end(self):
        node = TextNode(
            "Text ending with ![end image](https://example.com/end.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "https://example.com/end.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_only_image(self):
        node = TextNode("![only](https://example.com/only.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only", TextType.IMAGE, "https://example.com/only.png")
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Already bold", TextType.BOLD)]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("First ![img1](url1.png) here", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Second ![img2](url2.png) here", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1.png"),
            TextNode(" here", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.png"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_single(self):
        node = TextNode("Click [here](https://example.com) to visit", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" to visit", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_no_links(self):
        node = TextNode("Plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("Plain text with no links", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_at_start(self):
        node = TextNode("[Start link](https://start.com) then text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Start link", TextType.LINK, "https://start.com"),
            TextNode(" then text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_at_end(self):
        node = TextNode("Text ending with [end link](https://end.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://end.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_only_link(self):
        node = TextNode("[only](https://only.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("only", TextType.LINK, "https://only.com")]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_non_text_node(self):
        node = TextNode("Already code", TextType.CODE)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("Already code", TextType.CODE)]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_ignores_images(self):
        node = TextNode(
            "A [link](https://link.com) and ![image](https://img.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://link.com"),
            TextNode(" and ![image](https://img.png)", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_with_query_params(self):
        node = TextNode(
            "Search on [Google](https://google.com/search?q=python&lang=en) now",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Search on ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com/search?q=python&lang=en"),
            TextNode(" now", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)


if __name__ == "__main__":
    unittest.main()
