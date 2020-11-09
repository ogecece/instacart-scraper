import json

from parsel import Selector


class Page:
    def __init__(self, content):
        self.content = content

    @classmethod
    def from_response(cls, response):
        return cls(content=response)


class HtmlPage(Page):
    @classmethod
    def from_html(cls, html_response):
        return cls(content=Selector(html_response))


class JsonPage(Page):
    @classmethod
    def from_json(cls, json_response):
        return cls(content=json.loads(json_response))
