import unittest

from textnode import TextNode, TextType
from functions import text_node_to_html_node, split_nodes_delimiter, extract_md_images, extract_md_links, \
    split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_invalid_text_type(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a text node", text_type="plaintext")
            text_node_to_html_node(node)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(split_nodes, expected_output)

    def test_no_match(self):
        node = TextNode("This is a text node", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [node]
        self.assertEqual(split_nodes, expected_output)


class TestMDExtract(unittest.TestCase):
    def test_extract_md_images(self):
        matches = extract_md_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_many_imgs(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_md_images(text)
        self.assertEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_md_links(self):
        matches = extract_md_links(
            "This is text with an [some text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("some text", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_many_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_md_links(text)
        self.assertEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_no_match(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_md_images(text)
        self.assertListEqual([], matches)
        


class TestSplitImgsandLinks(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected_output = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]
        self.assertListEqual(expected_output, new_nodes)

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and a [second external link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "second external link",
                    TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_trailing_str(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and a [second external link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        node = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode(
                "second external link",
                TextType.LINK,
                "https://i.imgur.com/3elNhQu.png",
            ),
            TextNode("", TextType.TEXT),
        ]
        self.assertFalse(new_nodes == node)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
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
        alice = text_to_textnodes(text)
        self.assertListEqual(alice, expected_output)


class TestMDToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """        
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_md_to_blocks(self):
        text = """
            # This is a heading

            This is a paragraph of text.
            It has some **bold** and _italic_ words inside of it.
            
            - This is the first list item in a list block
            - This is a list item
            - This is another list item
        """
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks, 
            [
                "# This is a heading",
                "This is a paragraph of text.\nIt has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "###### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_sequential_ol(self):
        block = "1. This is a list\n3. This list is numbered incorrectly\n5. This should appear as a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. This is a list\n2. This list is numbered incorrectly\n3. This should appear as a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_unordered_list(self):
        block = "- This is a list\n- This list is numbered correctly\n- This should appear as an ordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_code(self):
        block = "```\nprint('Hello world')\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        block = "> I have no special talent. I am only passionately curious.\n> - Albert Einstein"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)