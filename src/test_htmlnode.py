import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="link", props={"href": "https://www.example.com", "target": "_blank"})

    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")

    def test_props(self):
        node = HTMLNode("a", "GitLab", props={
            "href": "https://gitlab.com",
            "target": "_blank"
            })
        self.assertEqual(node.props_to_html(), ' href="https://gitlab.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


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

