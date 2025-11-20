from textnode import *
from htmlnode import *

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
