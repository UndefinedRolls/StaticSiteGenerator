import unittest

from html_helpers import *

class text2HTML(unittest.TestCase):
    def test_1(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_2(self):
        self.maxDiff = None
        md = """
# This is **bolded** paragraph

## text in a p

### tag here

#### This is another paragraph with _italic_ text and `code` here

##### And another

###### And a final one
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>This is <b>bolded</b> paragraph</h1><h2>text in a p</h2><h3>tag here</h3><h4>This is another paragraph with <i>italic</i> text and <code>code</code> here</h4><h5>And another</h5><h6>And a final one</h6></div>",
        )

    def test_3(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
        self.maxDiff = None
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_4(self):
        md = """
    >This is a
    >**Block** Quote
    >By Me
    """
        self.maxDiff = None
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>Block</b> Quote By Me</blockquote></div>",
        )
    def test_5(self):
        md = """
    - This is a
    - **Unordered** List
    - By _Me_  
    """
        self.maxDiff = None
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a</li><li><b>Unordered</b> List</li><li>By <i>Me</i></li></ul></div>",
        )
    def test_6(self):
        md = """
    1. This is a
    2. **Ordered** List
    3. By _Me_
    """
        self.maxDiff = None
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a</li><li><b>Ordered</b> List</li><li>By <i>Me</i></li></ol></div>",
        )