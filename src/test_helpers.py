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


if __name__ == "__main__":
    unittest.main()