# import re
# from enum import Enum
from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    all_new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) == 0 or node.text.count(delimiter) % 2 != 0:
            new_nodes = [node]
        else:
            split_text = node.text.split(delimiter)
            node1 = TextNode(text=split_text[0], text_type=node.text_type)
            d_node = TextNode(text=split_text[1], text_type=text_type)
            node3 = TextNode(text=split_text[2], text_type=node.text_type)
            new_nodes = [node1, d_node, node3]
        all_new_nodes.extend(new_nodes)
    return all_new_nodes
