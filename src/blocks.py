from enum import Enum
from helpers import *

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    raw_blocks = markdown.replace("  ", "").split("\n\n")
    blocks = []
    for block in raw_blocks:
        cleaned = block.strip()
        if cleaned != "":
            blocks.append(cleaned)
    return blocks

def block_to_block_type(markdown):
    if not markdown:
        return BlockType.PARAGRAPH
    parts = markdown.split("\n")
    if is_heading(parts[0]):
        return BlockType.HEADING
    if is_code_block(markdown):
        return BlockType.CODE
    if is_quote(parts):
        return BlockType.QUOTE
    if is_unordered_list(parts):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(parts):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def extract_title(markdown):
    block_list = markdown_to_blocks(markdown)
    for block in block_list:
        if block_to_block_type(block) == BlockType.HEADING:
            marks, line = split_heading(block)
            if marks == 1:
                return line
    raise Exception("Could not extract title")
