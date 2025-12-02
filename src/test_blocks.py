from blocks import *
import unittest

class TextMarkdowntoBlocks(unittest.TestCase):
    def test_1(self):
        md = "# This is a heading"
        self.assertEqual(
            block_to_block_type(md),
            BlockType.HEADING,
        )
    def test_2(self):
        md = "## This is a heading"
        self.assertEqual(
            block_to_block_type(md),
            BlockType.HEADING,
        )

    def test_3(self):
        md = "### #This is a heading"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.HEADING,
            )
    def test_4(self):
        md = "#### This is a heading"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.HEADING,
            )
    def test_5(self):
        md = "##### This is a heading"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.HEADING,
            )
    def test_6(self):
        md = "###### This is a heading"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.HEADING,
            )
    def test_7(self):
        md = "######This is a paragraph"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.PARAGRAPH,
            )
    def test_8(self):
        md = "#This is a paragraph"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.PARAGRAPH,
            )
    def test_9(self):
        md = "```#This is a code```"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.CODE,
            )
    def test_10(self):
        md = ">This is a quote\n>that is on two lines"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.QUOTE,
            )
    def test_11(self):
        md = ">This is a quote\nthat was sent incorrectly"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.PARAGRAPH,
            )
    def test_12(self):
        md = "- This is an unordered list\n- with an item"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.UNORDERED_LIST,
        )
    def test_13(self):
        md = "- This is an unordered list\nwith an invalid item"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.PARAGRAPH,
        )
    def test_14(self):
        md = "1. This is an ordered list\n2. with an item"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.ORDERED_LIST,
        )
    def test_15(self):
        md = "1. This is an ordered list\n2. with an item\n3. and another item"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.ORDERED_LIST,
        )
    def test_16(self):
        md = "1. This is an ordered list\n2. with an item\nand another invalid item"
        self.assertEqual(
                block_to_block_type(md),
                BlockType.PARAGRAPH,
        )