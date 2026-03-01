import re
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


def extract_md_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_md_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    all_new_nodes = []
    for node in old_nodes:
        node_images = extract_md_images(node.text)
        if len(node_images) == 0:
            new_nodes = [node]
        else:
            new_nodes = []
            node_text = node.text
            for img in node_images:
                split_text = node_text.split(f"![{img[0]}]({img[1]})")
                if node_text.startswith("!["):
                    new_nodes.append(TextNode(text=img[0], text_type=TextType.IMAGE, url=img[1]))
                else:
                    new_nodes.extend(
                        [TextNode(text=split_text[0], text_type=node.text_type),
                         TextNode(text=img[0], text_type=TextType.IMAGE, url=img[1])
                         ]
                    )
                node_text = split_text[1]
            if len(node_text) > 0:
                new_nodes.append(TextNode(text=node_text, text_type=node.text_type))
        all_new_nodes.extend(new_nodes)
    return all_new_nodes


def split_nodes_link(old_nodes):
    all_new_nodes = []
    for node in old_nodes:
        node_links = extract_md_links(node.text)
        if len(node_links) == 0:
            new_nodes = [node]
        else:
            new_nodes = []
            node_text = node.text
            for lnk in node_links:
                split_text = node_text.split(f"[{lnk[0]}]({lnk[1]})")
                if node_text.startswith(f"[{lnk}]"):
                    new_nodes.append(TextNode(text=lnk[0], text_type=TextType.LINK, url=lnk[1]))
                else:
                    new_nodes.extend(
                        [TextNode(text=split_text[0], text_type=TextType.TEXT),
                         TextNode(text=lnk[0], text_type=TextType.LINK, url=lnk[1])
                         ]
                    )
                node_text = split_text[1]
            if node_text != "":
                new_nodes.append(TextNode(text=node_text, text_type=TextType.TEXT))
        all_new_nodes.extend(new_nodes)
    return all_new_nodes


def text_to_textnodes(text):
    node = TextNode(text=text, text_type=TextType.TEXT)
    images_and_text = split_nodes_image([node])
    add_link_nodes = split_nodes_link(images_and_text)
    add_code_nodes = split_nodes_delimiter(add_link_nodes,"`", TextType.CODE)
    add_itc_nodes = split_nodes_delimiter(add_code_nodes,"_", TextType.ITALIC)
    all_nodes = split_nodes_delimiter(add_itc_nodes,"**", TextType.BOLD)
    return all_nodes


def markdown_to_blocks(markdown_text):
    blocks = markdown_text.strip().split("\n\n")
    for block in blocks:
        blocks[blocks.index(block)] = "\n".join([new_block.strip().replace("\n", "") for new_block in block.split("\n")])
    new_blocks = []
    for item in blocks:
        new_blocks.extend(item.split("\n\n"))
    return new_blocks