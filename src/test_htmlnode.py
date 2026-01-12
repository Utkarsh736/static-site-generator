import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')
    
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            props={
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        result = node.props_to_html()
        # Check for leading space and both attributes
        self.assertTrue(result.startswith(" "))
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)
    
    def test_props_to_html_empty_props(self):
        node = HTMLNode("p", props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_none_props(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")
    
    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_repr(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://www.boot.dev"})
        self.assertEqual(
            repr(node),
            "HTMLNode(a, Click me, None, {'href': 'https://www.boot.dev'})"
        )
    
    def test_node_with_children(self):
        child1 = HTMLNode("span", "Hello")
        child2 = HTMLNode("span", "World")
        parent = HTMLNode("div", children=[child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.value, None)


if __name__ == "__main__":
    unittest.main()

