from blocks import *
import unittest

class TestBlocktoBlockType(unittest.TestCase):
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

class TestMarkdowntoBlocks(unittest.TestCase):
    def test_1(self):
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
    def test_2(self):
            md = """
- This is a list
- with items

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "- This is a list\n- with items",
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",

                ],
            )
    def test_3(self):
            md = """
- This is a list
- with items

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "- This is a list\n- with items",
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)",

                ],
            )
    def test_4(self):
            md = """
1. This is an ordered list
2. with items
and a new line in the same paragraph

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "1. This is an ordered list\n2. with items\nand a new line in the same paragraph",
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)",

                ],
            )
    def test_5(self):
            md = ""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                ],
            )
    def test_6(self):
            md = " \n\n "
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [],
            )

    def test_7(self):
        md = " \n\n  \n\n  beans\n\n "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["beans"],
        )
    def test_8(self):
        md = "Just me, all alone"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just me, all alone"],
        )

    def test_9(self):
        md = "Just me\n\n all alone"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just me", "all alone"],
        )
    def test_10(self):
        md = "Just me\n all\nalone"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just me\n all\nalone"],
        )
    def test_11(self):
        md = "Just me\n\n\n\nall alone"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just me", "all alone"],
        )
    def test_12(self):
        md = "\n\nJust me\n\n\n\nall alone\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just me", "all alone"],
        )
class TestExtractTitle(unittest.TestCase):
    def test_1(self):
        md = """
        # This is a good title
        
        - and an unordered list
        - because I should mix things up
        - sometimes
        
        # Dontchaknow?
        """
        header = extract_title(md)
        self.assertEqual(header, "This is a good title")

    def test_2(self):
        md = """
        ## This is a bad title

        - and an unordered list
        - because I should mix things up
        - sometimes

        # Dontchaknow?
        """
        header = extract_title(md)
        self.assertEqual(header, "Dontchaknow?")
    def test_3(self):
        md = """
        ## This is a bad title

        - and an unordered list
        - because I should mix things up
        - sometimes

        ### Dontchaknow?
        """

        self.assertRaises(Exception, extract_title, md)