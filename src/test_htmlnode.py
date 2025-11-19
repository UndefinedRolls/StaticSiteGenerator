import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_1(self):
        prop = HTMLNode(props={"href": "https://google.com"})
        expected_value = 'href="https://google.com" '
        self.assertEqual(prop.props_to_html(), expected_value)
    def test_2(self):
        prop = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        expected_value = 'href="https://google.com" target="_blank" '
        self.assertEqual(prop.props_to_html(), expected_value)
    def test_3(self):
        prop = HTMLNode(props={"a": "https://google.com", "b": "I am an orange", "c": "./orange"})
        expected_value = 'a="https://google.com" b="I am an orange" c="./orange" '
        self.assertEqual(prop.props_to_html(), expected_value)
    def test_4(self):
        prop = HTMLNode(tag="p", value="I saw her standing here", children="a", props={"a": "https://google.com", "b": "I am an orange", "c": "./orange"})
        expected_value = 'Tag:p Value:I saw her standing here Children:a Props:a="https://google.com" b="I am an orange" c="./orange" '
        self.assertEqual(repr(prop), expected_value)