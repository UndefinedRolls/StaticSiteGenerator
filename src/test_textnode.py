import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_bold_italic_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_url_eq(self):
        node = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)
    def test_url_neq(self):
        node = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a link node", TextType.LINK, "https://boots.dev")
        self.assertNotEqual(node, node2)
    def test_italic_eq(self):
        node = TextNode("This is a link node", TextType.ITALIC, None)
        node2 = TextNode("This is a link node", TextType.ITALIC, None)
        self.assertEqual(node, node2)
    def test_italic_link_neq(self):
        node = TextNode("This is a link node", TextType.ITALIC, "https://boot.dev")
        node2 = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)
    def test_img_eq(self):
        node = TextNode("This is a link node", TextType.IMAGE)
        node2 = TextNode("This is a link node", TextType.IMAGE)
        self.assertEqual(node, node2)
    def test_code_eq(self):
        node = TextNode("This is a link node", TextType.CODE)
        node2 = TextNode("This is a link node", TextType.CODE)
        self.assertEqual(node, node2)
    def test_img_code_neq(self):
        node = TextNode("This is a link node", TextType.IMAGE)
        node2 = TextNode("This is a link node", TextType.CODE)
        self.assertNotEqual(node, node2)
    def test_plain_eq(self):
        node = TextNode("This is a link node", TextType.PLAIN)
        node2 = TextNode("This is a link node", TextType.PLAIN)
        self.assertEqual(node, node2)




if __name__ == "__main__":
    unittest.main()