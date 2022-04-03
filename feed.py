import os
import json
import requests
from pathlib import Path
import xml.etree.ElementTree as ET


downloads_path = str(Path.home() / "Downloads")


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


def extract_episode_num(title):
    nums = list(filter(lambda x: x.isnumeric(), title.split(" ")))
    return nums[-1]


def filter_local_files(keywords, bangumis, folder_path):
    filenames = list(
        filter(
            lambda filename: all(map(lambda x: x in filename, keywords)),
            os.listdir(folder_path),
        )
    )
    existed_episode = [extract_episode_num(filename) for filename in filenames]
    return list(
        filter(
            lambda x: extract_episode_num(x["title"]) not in existed_episode, bangumis
        )
    )


class Feeder:
    def __init__(self, download_folder=downloads_path):
        self.rss_url = "https://bangumi.moe/rss/latest"
        self.search_url = "https://bangumi.moe/api/v2/torrent/search"
        self.download_folder = download_folder

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
        return swap_link_with_magnet(
            filter_local_files(
                keywords,
                list(
                    filter(
                        lambda bangumi: all(
                            map(lambda x: x in bangumi["title"], keywords)
                        ),
                        bangumis,
                    )
                ),
                self.download_folder,
            )
        )

    def search_archive(self, query, keywords):
        resp = requests.post(self.search_url, json={"query": query})
        torrents = json.loads(resp.content)["torrents"]
        return filter_local_files(
            keywords,
            list(
                map(
                    lambda x: {"title": x["title"], "magnet": x["magnet"]},
                    filter(
                        lambda bangumi: all(
                            map(lambda x: x in bangumi["title"], keywords)
                        ),
                        torrents,
                    ),
                )
            ),
            self.download_folder,
        )
