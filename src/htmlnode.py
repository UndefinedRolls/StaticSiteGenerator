class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        prop = ""
        if not self.props:
            return ""
        for key in self.props.keys():
            value = self.props[key]
            prop += f' {key}="{value}"'
        return prop
    def __repr__(self):
        return f'Tag:{self.tag} Value:{self.value} Children:{self.children} Props:{self.props_to_html()}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None, children=None):
        if children is not None:
            raise TypeError("Leaf node does not accept child nodes")
        if value is None:
            raise ValueError("value is required")
        super(LeafNode, self).__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, value=None, props=None):
        if value is not None:
            raise TypeError("Parent node does not accept a value")
        if children is None:
            raise ValueError("Parent node requires children")
        if tag is None:
            raise ValueError("Parent Node requires a tag")
        super(ParentNode, self).__init__(tag=tag, children=children, props=props, value=None)

    def to_html(self):
        html_block = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html_block += child.to_html()
        html_block += f'</{self.tag}>'
        return html_block



if __name__ == "__main__":
    unittest.main()
