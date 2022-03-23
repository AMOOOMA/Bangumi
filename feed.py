import requests
import xml.etree.ElementTree as ET


class Feeder:
    def __init__(self):
        self.rss_url = "https://bangumi.moe/rss/latest"

    def read_latest(self):
        content = requests.get(self.rss_url).content
        tree = ET.fromstring(content)
        bangumis = []
        for item in tree.iter("item"):
            bangumi = {"title": item.find("title").text, "link": item.find("link").text}
            bangumis.append(bangumi)

        return bangumis

    def read_with_keywords(self, keywords):
        bangumis = self.read_latest()
        return list(
            filter(
                lambda bangumi: all(map(lambda x: x in bangumi["title"], keywords)),
                bangumis,
            )
        )
