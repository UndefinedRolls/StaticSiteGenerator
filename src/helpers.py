from textnode import *
from htmlnode import *
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case _:
            raise Exception("An Error Occurred")


def split_nodes_delimited(old_nodes, delimiter, text_type):
    new_nodes = []
    temp_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN or node.text.count(delimiter) == 0:
            new_nodes.append(node)
        else:
            new_text = node.text.split(delimiter)
            if node.text.count(delimiter) % 2 != 0:
                raise Exception("invalid Markdown syntax")
            for i in range(len(new_text)):
                if new_text[i] != "":
                    if i % 2 == 1:
                        temp_nodes.append(TextNode(new_text[i], text_type))
                    else:
                        temp_nodes.append(TextNode(new_text[i], TextType.PLAIN))
            new_nodes.extend(temp_nodes)
    return new_nodes

def extract_markdown_images(text):
    markdown_tuples = []
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for i in range(len(images)):
        markdown_tuples.append(images[i])
    return markdown_tuples

def extract_markdown_links(text):
    markdown_tuples = []
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for i in range(len(links)):
        markdown_tuples.append(links[i])
    return markdown_tuples

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            markdown_split = extract_markdown_images(node.text)
            new_nodes.extend(split_nodes_helper(text = original_text, text_type = TextType.IMAGE, matches = markdown_split,delimiter = "!["))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            markdown_split = extract_markdown_links(node.text)
            new_nodes.extend(split_nodes_helper(text = original_text, text_type = TextType.LINK, matches = markdown_split,delimiter = "["))
    return new_nodes

def split_nodes_helper(text, text_type, matches, delimiter):
    new_nodes = []
    for alt, url in matches:
        split_text = text.split(f"{delimiter}{alt}]({url})", 1)
        text = split_text[-1]
        if split_text[0] != "":
            new_nodes.append(TextNode(split_text[0], TextType.PLAIN))
        new_nodes.append(TextNode(alt, text_type, url))
    if text:
        new_nodes.append(TextNode(text, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = []
    text_node = TextNode(text, TextType.PLAIN)
    new_nodes.append(text_node)
    new_nodes = split_nodes_delimited(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimited(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimited(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_links(new_nodes)
    return new_nodes

def is_heading(line):
    if not line.startswith("#"):
        return False
    marks, _ = split_heading(line)
    if not (1 <= marks <= 6):
        return False
    return len(line) > marks and line[marks] == " "
def is_code_block(markdown):
    return markdown.startswith("```") and markdown.endswith("```")
def is_quote(lines):
    return all(line.strip().startswith(">") for line in lines)
def is_unordered_list(lines):
    return all(line.lstrip().startswith("- ") for line in lines)
def is_ordered_list(lines):
    order = 1
    for line in lines:
        if not line.lstrip().startswith(f"{order}. "):
            return False
        order += 1
    return True

def text_to_children(text, replacements, tag = "p") :
    text = apply_replacements(text, replacements)
    node_list = text_to_textnodes(text)
    child_nodes= []
    for node in node_list:
        child_nodes.append(text_node_to_html_node(node))
    return ParentNode(tag, children=child_nodes)

def list_block_to_parent(block, parent_tag, bullet_prefix = None):
    items = block.split("\n")
    children = []
    for i, text in enumerate(items, start = 1):
        item = text.strip()
        replacements = [("  ", "")]
        if bullet_prefix is not None:
            replacements.insert(0, (bullet_prefix, ""))
        else:
            replacements.insert(0, (f"{i}. ", ""))
        children.append(text_to_children(item, replacements, "li"))
    return ParentNode(parent_tag, children=children)

def split_heading(block):
    marks = 0
    for mark in block:
        if mark == "#":
            marks += 1
        else:
            break
    text = block[marks +1:]
    return marks, text

def apply_replacements(text, replacements):
    for old, new in replacements:
        text = text.replace(old, new)
    return text

