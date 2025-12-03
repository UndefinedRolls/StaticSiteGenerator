from helpers import *
from blocks import *
from htmlnode import *
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child_nodes = []
        match block_type:
            case BlockType.PARAGRAPH:
                html_nodes.append(text_to_children(block, [("\n", " ")]))
            case BlockType.HEADING:
                marks, text = split_heading(block)
                html_nodes.append(text_to_children(text, [("\n", "")], f"h{marks}"))
            case BlockType.CODE:
                text = apply_replacements(block, [("```\n", ""),
                                                  ("```", ""),
                                                  ("  ", "")])
                child = LeafNode(value=text, tag="code")
                html_nodes.append(ParentNode("pre", children = [child]))
            case BlockType.QUOTE:
                html_nodes.append(text_to_children(block, [("\n", " "), (">", ""), ("  ", "")], "blockquote"))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(list_block_to_parent(block, "ul", "- "))
            case BlockType.ORDERED_LIST:
                html_nodes.append(list_block_to_parent(block, "ol"))
            case _:
                pass
    return ParentNode("div", children = html_nodes)
