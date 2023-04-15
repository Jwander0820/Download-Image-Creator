from image_crawler import ImageCrawler


if __name__ == '__main__':
    token = "643a3cb3e843413991623437caf4ec85"
    url = f"https://www.bing.com/images/create/a-mystical-interstellar-creature2c-shaped-by-cluste/{token}?FORM=GUH2CR"

    crawler = ImageCrawler(url)
    crawler.run()
