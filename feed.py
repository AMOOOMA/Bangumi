import json
import requests
import xml.etree.ElementTree as ET


def swap_link_with_magnet(bangumis):
    for bangumi in bangumis:
        link = bangumi.pop("link", None)
        _id = link.split("/")[-1]
        torrent = json.loads(
            requests.post(
                "https://bangumi.moe/api/torrent/fetch", json={"_id": _id}
            ).content
        )
        bangumi["magnet"] = torrent["magnet"]


class Feeder:
    def __init__(self):
        self.rss_url = "https://bangumi.moe/rss/latest"
        self.search_url = "https://bangumi.moe/api/v2/torrent/search"

    def read_latest(self):
        content = requests.get(self.rss_url).content
        tree = ET.fromstring(content)
        bangumis = []
        for item in tree.iter("item"):
            bangumi = {"title": item.find("title").text, "link": item.find("link").text}
            bangumis.append(bangumi)

        return bangumis

    def read_latest_with_keywords(self, keywords):
        bangumis = self.read_latest()
        return list(
            filter(
                lambda bangumi: all(map(lambda x: x in bangumi["title"], keywords)),
                bangumis,
            )
        )

    def search_archive(self, query, keywords):
        resp = requests.post(self.search_url, json={"query": query})
        torrents = json.loads(resp.content)["torrents"]
        return list(
            map(
                lambda x: {"title": x["title"], "magnet": x["magnet"]},
                filter(
                    lambda bangumi: all(map(lambda x: x in bangumi["title"], keywords)),
                    torrents,
                ),
            )
        )
