from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    IMAGE = "image"
    LINK = "link"


class TextNode:
    def __init__(self, text, test_type, url=None):
        self.text = text
        self.test_type = test_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and self.test_type == other.test_type and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.test_type}, {self.url})"

