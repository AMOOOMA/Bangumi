from feed import Feeder


def main():
    feeder = Feeder()
    feeder.read_latest()
    print(feeder.read_with_keywords(["Lilith-Raws", "秘密內幕 女警的反擊"]))


if __name__ == "__main__":
    main()