import os
import re
from enum import Enum
from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(text_block):
    block = text_block.strip()
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r'^```[^`{3}]+?```$', block): # and re.match(r'```$', block):
        return BlockType.CODE
    elif all([re.match(r'^>', line) for line in block.splitlines()]):
        return BlockType.QUOTE
    elif all([re.match("^- ", line) for line in block.splitlines()]):
        return BlockType.UNORDERED_LIST
    elif all([re.match(r'\d\.\s', line) for line in block.splitlines()]):
        prev = 0
        for line in block.splitlines():
            if int(line.split(".")[0]) != prev + 1:
                return BlockType.PARAGRAPH
            prev = int(line.split(".")[0])
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


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
        if node.text.count(delimiter) == 0 or node.text.count(delimiter) % 2 != 0 or node.text_type == TextType.CODE:
            new_nodes = [node]
        else:
            if delimiter == "```":
                new_nodes = [TextNode(text=re.sub(r'^```\n', '', node.text), text_type=text_type)]
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


def markdown_to_html_nodes(markdown_text):
    new_nodes = []
    markdown_blocks = markdown_to_blocks(markdown_text)
    for md_block in markdown_blocks:
        match block_to_block_type(md_block):
            case BlockType.HEADING:
                new_nodes.append(LeafNode(tag=f"h{len(re.match(r'^#{1,6}', md_block).group())}", value=re.sub(r'^#{1,6} ', '', md_block)))
            case BlockType.CODE:
                new_nodes.append(ParentNode(tag="div", children=[ParentNode(tag="pre", children=[LeafNode(tag="code", value=re.sub(r'^```|```$', '', md_block).lstrip())])]))
            case BlockType.QUOTE:
                quote_value = "\n".join([re.sub(r'^>\s?', '', line) for line in md_block.splitlines()])
                new_nodes.append(LeafNode(tag="blockquote", value=quote_value))
            case BlockType.ORDERED_LIST:
                child_values = []
                lines = md_block.splitlines()
                for line in lines:
                    child_nodes = re.sub(r'\d\. ', '', "".join([text_node_to_html_node(node).to_html() for node in text_to_textnodes(line)]).strip())
                    child_values.append(LeafNode(tag="li", value=child_nodes))
                new_nodes.append(ParentNode(tag="ol", children=child_values))
            case BlockType.UNORDERED_LIST:
                child_values = []
                lines = md_block.splitlines()
                for line in lines:
                    child_nodes = re.sub(r'^- ', '', "".join([text_node_to_html_node(node).to_html() for node in text_to_textnodes(line)]).strip())
                    child_values.append(LeafNode(tag="li", value=child_nodes))
                new_nodes.append(ParentNode(tag="ul", children=child_values))
            case _:
                if "\n" in md_block:
                    md_block = "\n".join(md_block.splitlines())
                child_nodes = []
                text_nodes = text_to_textnodes(md_block)
                for node in text_nodes:
                    if len(node.text) > 0:
                        child_nodes.append(text_node_to_html_node(node))
                new_nodes.append(ParentNode(tag="div", children=[ParentNode(tag="p", children=child_nodes)]))
    return ParentNode(tag="div", children=[new_nodes])


def extract_title(markdown):
    md_title = re.findall(r'# (.+)', markdown)
    return md_title[0]


def generate_page(from_path, dest_path):
    abs_path = os.path.abspath(".") + "/" + "/".join(dest_path.split("/")[:-1])
    print(f"Generating page from {from_path} to {dest_path} using template.html")
    with open(from_path, "r") as md_file:
        markdown = md_file.read()
    html_node = markdown_to_html_nodes(markdown)
    page_title = extract_title(markdown)
    with open("template.html", "r") as template_file:
        html_template = template_file.read()
    with open(dest_path.rstrip(".md") + ".html", "w") as html_page:
        new_page = html_template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_node.to_html())
        html_page.write(new_page)
