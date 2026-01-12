import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
    
    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "A paragraph")],
            {"class": "container", "id": "main"}
        )
        html = node.to_html()
        self.assertIn("<div", html)
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertIn("<p>A paragraph</p>", html)
        self.assertIn("</div>", html)
    
    def test_to_html_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode("section", [
                    LeafNode("h1", "Title"),
                    LeafNode("p", "Content")
                ]),
                ParentNode("footer", [
                    LeafNode("span", "Footer text")
                ])
            ]
        )
        expected = "<div><section><h1>Title</h1><p>Content</p></section><footer><span>Footer text</span></footer></div>"
        self.assertEqual(node.to_html(), expected)
    
    def test_to_html_no_tag_raises_error(self):
        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("tag", str(context.exception).lower())
    
    def test_to_html_no_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("children", str(context.exception).lower())
    
    def test_to_html_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")
    
    def test_to_html_deeply_nested(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    ParentNode("p", [
                        LeafNode("b", "Deep"),
                        LeafNode(None, " nesting")
                    ])
                ])
            ])
        ])
        expected = "<div><section><article><p><b>Deep</b> nesting</p></article></section></div>"
        self.assertEqual(node.to_html(), expected)
    
    def test_repr(self):
        node = ParentNode("div", [LeafNode("p", "text")])
        repr_str = repr(node)
        self.assertIn("ParentNode", repr_str)
        self.assertIn("div", repr_str)


if __name__ == "__main__":
    unittest.main()

