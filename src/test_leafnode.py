import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")
    
    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "img",
            "",
            {"src": "image.jpg", "alt": "A description"}
        )
        html = node.to_html()
        self.assertIn('<img', html)
        self.assertIn('src="image.jpg"', html)
        self.assertIn('alt="A description"', html)
        self.assertIn('></img>', html)
    
    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")
    
    def test_leaf_to_html_italic(self):
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")
    
    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('hello')")
        self.assertEqual(node.to_html(), "<code>print('hello')</code>")
    
    def test_repr(self):
        node = LeafNode("a", "Link", {"href": "https://www.boot.dev"})
        self.assertEqual(
            repr(node),
            "LeafNode(a, Link, {'href': 'https://www.boot.dev'})"
        )


if __name__ == "__main__":
    unittest.main()

