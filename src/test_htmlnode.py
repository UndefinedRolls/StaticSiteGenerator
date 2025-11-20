import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_1(self):
        prop = HTMLNode(props={"href": "https://google.com"})
        expected_value = ' href="https://google.com"'
        self.assertEqual(prop.props_to_html(), expected_value)
    def test_2(self):
        prop = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        expected_value = ' href="https://google.com" target="_blank"'
        self.assertEqual(prop.props_to_html(), expected_value)
    def test_3(self):
        prop = HTMLNode(props={"a": "https://google.com", "b": "I am an orange", "c": "./orange"})
        expected_value = ' a="https://google.com" b="I am an orange" c="./orange"'
        self.assertEqual(prop.props_to_html(), expected_value)
    def test_4(self):
        prop = HTMLNode(tag="p", value="I saw her standing here", children="a", props={"a": "https://google.com", "b": "I am an orange", "c": "./orange"})
        expected_value = 'Tag:p Value:I saw her standing here Children:a Props: a="https://google.com" b="I am an orange" c="./orange"'
        self.assertEqual(repr(prop), expected_value)

class TestLeafNode(unittest.TestCase):
    def test_1(self):
        leaf = LeafNode(tag="p", value="This is a test")
        expected_value = '<p>This is a test</p>'
        self.assertEqual(leaf.to_html(), expected_value)
    def test_2(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)
    def test_3(self):
        leaf = LeafNode(tag=None, value="This is a test")
        expected_value = 'This is a test'
        self.assertEqual(leaf.to_html(), expected_value)
    def test_4(self):
        leaf = LeafNode(tag="a", value="Click me!", props={"href":"https://www.google.com"})
        expected_value = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leaf.to_html(), expected_value)
    def test_5(self):
        with self.assertRaises(TypeError):
            LeafNode(tag="p", value="Click me!", children=["<b>This was for real</b>"], props=None)

