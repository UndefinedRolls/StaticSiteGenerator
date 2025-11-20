import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
global LOREM_IPSUM
LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et \
dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip \
ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu \
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt \
mollit anim id est laborum"

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


class TestParentNode(unittest.TestCase):
    def test_1(self):
        parent = ParentNode(tag="p", children=[LeafNode("p", value=LOREM_IPSUM)])
        expected_value = f'<p><p>{LOREM_IPSUM}</p></p>'
        self.assertEqual(parent.to_html(), expected_value)
    def test_2(self):
        parent = ParentNode(tag="p", children=[LeafNode("b", "This is a test"),
                                               LeafNode("p", value=LOREM_IPSUM)])
        expected_value = f'<p><b>This is a test</b><p>{LOREM_IPSUM}</p></p>'
        self.assertEqual(parent.to_html(), expected_value)
    def test_3(self):
        parent = ParentNode(tag="p", children=[LeafNode("b", "This is a test"),
                                               LeafNode("p", value=LOREM_IPSUM),
                                               LeafNode("a", value="Source", props={"href": "https://loremipsum.io"})])
        expected_value = f'<p><b>This is a test</b><p>{LOREM_IPSUM}</p><a href="https://loremipsum.io">Source</a></p>'
        self.assertEqual(parent.to_html(), expected_value)
    def test_4(self):
        parent = ParentNode(tag="p", children=[LeafNode("b", "This is a test"),
                                               ParentNode("p", children=[LeafNode("p", value=LOREM_IPSUM),
                                                                         LeafNode("a", value="Source",
                                                                                  props={"href": "https://loremipsum.io"})])])
        expected_value = f'<p><b>This is a test</b><p><p>{LOREM_IPSUM}</p><a href="https://loremipsum.io">Source</a></p></p>'
        self.assertEqual(parent.to_html(), expected_value)
    def test_5(self):
        with self.assertRaises(TypeError):
            ParentNode(tag="p", value="Click me!", children=["<b>This was for real</b>"], props=None)
    def test_6(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="p", children=None, props=None)
    def test_7(self):
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=["<b>This was for real</b>"], props=None)
