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
        for key in self.props.keys():
            value = self.props[key]
            prop += f'{key}="{value}" '
        return prop
    def __repr__(self):
        return f'Tag:{self.tag} Value:{self.value} Children:{self.children} Props:{self.props_to_html()}'