class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_props = ""
        if self.props is not None:
            for prop in self.props:
                html_props += f' {prop}="{self.props[prop]}"'
        return html_props


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(self)
        self.tag = tag
        self.value = value
        self.props = props

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("All Leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires tag property")
        if self.children is None:
            raise ValueError("ParentNode requires children property")
        html_children = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{html_children}</{self.tag}>"
