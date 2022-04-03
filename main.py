from feed import Feeder


def main():
    feeder = Feeder()
    # print(feeder.read_latest())
    # print(feeder.read_latest_with_keywords(["Lilith-Raws", "秘密內幕 女警的反擊"]))
    print(feeder.search_archive("Lilith-Raws Odd Taxi", ["Lilith-Raws", "Odd Taxi"]))


if __name__ == "__main__":
    main()
