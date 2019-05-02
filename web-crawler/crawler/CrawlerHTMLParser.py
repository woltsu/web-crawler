from html.parser import HTMLParser

class CrawlerHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attributes):
        # Parse all links
        if (tag == "a"):
            self.parseAttributes(attributes)

    def parseAttributes(self, attributes):
        # Find the hrefs from links
        for attribute, value in attributes:
            if (attribute == "href"):
                self.links.append(value)

    def clear(self):
        self.links.clear()