import unittest

from src.htmlnode import HTMLNode


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


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props or {}
        self.children = []

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props}]))"

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires value property")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
