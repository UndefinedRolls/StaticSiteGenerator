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
    def test_8(self):
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
if __name__ == "__main__":
    unittest.main()