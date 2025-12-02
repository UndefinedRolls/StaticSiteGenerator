import unittest

from helpers import *
from textnode import *

class TestText2HTML(unittest.TestCase):
    def test_1(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_2(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    def test_3(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_4(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    def test_5(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://google.com"})
    def test_6(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="https://media.istockphoto.com/id/814423752/photo/eye-of-model-with-colorful-art-make-up-close-up.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://media.istockphoto.com/id/814423752/photo/eye-of-model-with-colorful-art-make-up-close-up.jpg",
                                           "alt": "This is an image node"})
    def test_7(self):
        with self.assertRaises(Exception):
            node = TextNode("This is an invalid node", "header1")
            text_node_to_html_node(node)


class TestMarkdown2Text(unittest.TestCase):
    def test_1(self):
        node = TextNode("This is a text node with a `code block` word", TextType.PLAIN)
        expected_results = [TextNode("This is a text node with a ", TextType.PLAIN), TextNode("code block", TextType.CODE), TextNode(" word", TextType.PLAIN)]
        new_nodes = split_nodes_delimited([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, expected_results)
    def test_2(self):
        node = TextNode("This is a text node with a **bold** word", TextType.PLAIN)
        expected_results = [TextNode("This is a text node with a ", TextType.PLAIN),
                            TextNode("bold", TextType.BOLD), TextNode(" word", TextType.PLAIN)]
        new_nodes = split_nodes_delimited([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, expected_results)
    def test_3(self):
        node = TextNode("This is a text node with a **bold** word at the **end**", TextType.PLAIN)
        expected_results = [TextNode("This is a text node with a ", TextType.PLAIN),
                            TextNode("bold", TextType.BOLD), TextNode(" word at the ", TextType.PLAIN), TextNode("end", TextType.BOLD)]
        new_nodes = split_nodes_delimited([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, expected_results)

    def test_4(self):
        node = TextNode("This is a text node with an _italic_ word", TextType.PLAIN)
        expected_results = [TextNode("This is a text node with an ", TextType.PLAIN),
                            TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.PLAIN)]
        new_nodes = split_nodes_delimited([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, expected_results)
    def test_5(self):
            node = TextNode("_This_ is a text node with an _italic_ word at the front", TextType.PLAIN)
            expected_results = [TextNode("This", TextType.ITALIC), TextNode(" is a text node with an ", TextType.PLAIN),
                                TextNode("italic", TextType.ITALIC), TextNode(" word at the front", TextType.PLAIN)]
            new_nodes = split_nodes_delimited([node], "_", TextType.ITALIC)
            self.assertEqual(new_nodes, expected_results)
    def test_6(self):
        with self.assertRaises(Exception):
            node = TextNode("_This_ is a text node with an _italic word at the front", TextType.PLAIN)
            split_nodes_delimited([node], "_", TextType.ITALIC)

class TestMarkdownImagesAndText(unittest.TestCase):
    def test_1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
    def text_2(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    def test_3(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_4(self):
        matches = extract_markdown_links(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_5(self):
        matches = extract_markdown_images("Just plain text, no images here.")
        self.assertEqual([], matches)
    def test_6(self):
        text = "An image ![alt](https://example.com/a.png) and a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertEqual([("link", "https://example.com")], matches)
    def test_7(self):
        matches = extract_markdown_images("A [link](https://example.com) only.")
        self.assertEqual([], matches)
    def test_8(self):
        text = "Go [here](https://example.com), then [there](https://example.org)."
        matches = extract_markdown_links(text)
        self.assertEqual(
            [("here", "https://example.com"), ("there", "https://example.org")],
            matches,
        )
    def test_9(self):
        text = "Watch [video](https://example.com/watch?v=abc123&x=1)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            [("video", "https://example.com/watch?v=abc123&x=1")],
            matches,
        )
    def test_10(self):
        text = "First [one](https://one.com)\nSecond [two](https://two.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            [("one", "https://one.com"), ("two", "https://two.com")],
            matches,
        )


class TestCreateImageNodes(unittest.TestCase):
    def test_1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
    def test_2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_3(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with left over text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ), TextNode(" with left over text", TextType.PLAIN),
            ],
            new_nodes,
        )
    def test_4(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is an image at the start of the text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is an image at the start of the text", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_5(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and yet another ![third image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and yet another ", TextType.PLAIN),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )

    def test_6(self):
        node = TextNode(
            "This is text with no images",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.PLAIN)
            ],
            new_nodes,
        )
    def test_7(self):
        node = [TextNode(
            "This is text with no images",
            TextType.PLAIN,
        ), TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        ), TextNode(
            "This is bold text",
            TextType.BOLD
        )]
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.PLAIN),
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is bold text", TextType.BOLD)
            ],
            new_nodes,
        )
    def test_8(self):
        node = TextNode(
            "This is text with an image ![](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.PLAIN),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
    def test_9(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

class TestCreateLinkNodes(unittest.TestCase):
    def test_1(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
    def test_2(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_3(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) with left over text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ), TextNode(" with left over text", TextType.PLAIN),
            ],
            new_nodes,
        )
    def test_4(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) is an link at the start of the text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is an link at the start of the text", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_5(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and yet another [third link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and yet another ", TextType.PLAIN),
                TextNode(
                    "third link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )

    def test_6(self):
        node = TextNode(
            "This is text with no images",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.PLAIN)
            ],
            new_nodes,
        )
    def test_7(self):
        node = [TextNode(
            "This is text with no images",
            TextType.PLAIN,
        ), TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        ), TextNode(
            "This is bold text",
            TextType.BOLD
        )]
        new_nodes = split_nodes_links(node)
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.PLAIN),
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is bold text", TextType.BOLD)
            ],
            new_nodes,
        )
    def test_8(self):
        node = TextNode(
            "This is text with an link [](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an link ", TextType.PLAIN),
                TextNode("", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
    def test_9(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

class TestTexttoNodes(unittest.TestCase):
    def test_1(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [

                    TextNode("This is ", TextType.PLAIN),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.PLAIN),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.PLAIN),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.PLAIN),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.PLAIN),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
            nodes,
        )
    def test_1(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [

                    TextNode("This is ", TextType.PLAIN),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.PLAIN),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.PLAIN),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.PLAIN),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.PLAIN),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
            nodes,
        )
    def test_2(self):
        nodes = text_to_textnodes("This is _text_ with an **italic** word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a `code block` and a [link](https://boot.dev)")
        self.assertListEqual(
            [

                    TextNode("This is ", TextType.PLAIN),
                    TextNode("text", TextType.ITALIC),
                    TextNode(" with an ", TextType.PLAIN),
                    TextNode("italic", TextType.BOLD),
                    TextNode(" word and an ", TextType.PLAIN),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.PLAIN),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and a ", TextType.PLAIN),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
            nodes,
        )
    def test_3(self):
        nodes = text_to_textnodes("")
        self.assertListEqual(
            [

            ],
            nodes,
        )
    def test_4(self):
        nodes = text_to_textnodes("**This is _nested text_ with an **italic** word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a `code block` and a [link](https://boot.dev)**")
        self.maxDiff=None
        self.assertListEqual(
            [
            TextNode("This is _nested text_ with an ", TextType.BOLD),
            TextNode("italic", TextType.PLAIN),
            TextNode(" word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a `code block` and a [link](https://boot.dev)", TextType.BOLD),
], nodes
        )
    def test_5(self):
        nodes = text_to_textnodes("**This is only bold text**")
        self.maxDiff=None
        self.assertListEqual(
            [
            TextNode("This is only bold text", TextType.BOLD)]
            , nodes
        )
    def test_6(self):
        nodes = text_to_textnodes("**This is only bold text ****Next to Bold Text**")
        self.maxDiff=None
        self.assertListEqual(
            [
            TextNode("This is only bold text ", TextType.BOLD),
            TextNode("Next to Bold Text", TextType.BOLD)]
            , nodes
        )

class TextMarkdowntoBlocks(unittest.TestCase):
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

