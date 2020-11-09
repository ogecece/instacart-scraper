import json
from urllib.parse import unquote

import jmespath

from data_collection.scraping.page import HtmlPage, JsonPage


class HomePage(HtmlPage):
    def auth_token(self):
        return self.content.css("meta[name=csrf-token]").attrib["content"]

    def sitekey(self):
        sitekey_json = json.loads(self.content.css("script#node-gon::text").get())
        sitekey_path = jmespath.compile(
            "landingContainer.container_payload.container.modules[*].data.sitekey | [0]"
        )
        return sitekey_path.search(sitekey_json)


class SelectStorePage(HtmlPage):
    def store_url(self):
        store_content_script = self.content.css(
            "script#node-initial-bundle::text"
        ).get()
        store_content_json = json.loads(unquote(store_content_script))
        store_metadata = store_content_json["bundle"]["current_retailer"]
        return {
            "store_slug": store_metadata["slug"],
            "store_name": store_metadata["name"],
            "store_logo_url": store_metadata["logo"]["url"],
        }


class StorePage(JsonPage):
    def shelves(self):
        path = jmespath.compile(
            "container.modules[*].{name: data.header.label, href: async_data_path}[?href!=`null`]"
        )
        return path.search(self.content)


class ShelfPage(JsonPage):
    def items_names(self):
        path = jmespath.compile("module_data.items[*].name")
        return list(set(path.search(self.content)))
