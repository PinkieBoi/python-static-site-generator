import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_all_params(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        expected_vals = ["This is a text node", "link", "https://example.com"]
        self.assertEqual([node.text, node.text_type.value, node.url], expected_vals)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_type(self):
        mynode = TextNode(
            text="This is a text node",
            text_type=TextType.LINK,
            url="https://example.com",
        )
        self.assertStartsWith(mynode.url, "http")



if __name__ == "__main__":
    unittest.main()