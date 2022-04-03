from feed import Feeder, filter_local_files


def main():
    feeder = Feeder()
    # print(feeder.read_latest())
    # print(feeder.read_latest_with_keywords(["Lilith-Raws", "秘密內幕 女警的反擊"]))
    keywords = ["Lilith-Raws", "Eighty Six"]
    print(
        filter_local_files(
            keywords, feeder.search_archive("Lilith-Raws Eighty Six", keywords)
        )
    )


if __name__ == "__main__":
    main()
