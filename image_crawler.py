import os
import re
import json
import requests
from bs4 import BeautifulSoup
from logger import log_filter, create_logger

DEFAULT_FOLDER = "img"


class ImageCrawler:
    def __init__(self, url: str, visited_urls_file="visited_urls.json"):
        """
        初始化 ImageCrawler 類。

        :param url: 要爬取的網站的 URL。
        :param visited_urls_file: 用於存儲已訪問網址的 JSON 文件。
        """
        self.logger = create_logger()
        self.url = url
        self.visited_urls_file = visited_urls_file
        self.img_urls = []
        self.trans_img_urls = []
        self.img_prompt = ""

    def run(self, folder_name="img"):
        """
        如果當前網址尚未被訪問，則執行爬取和下載圖片的過程。
        """
        try:
            if not self.check_visited():
                self.crawl_images()
                self.download_images(folder_name)
                self.mark_visited()
                text = f"已成功下載 {self.url}"
            else:
                text = f"圖片已存在 {self.url}"
        except Exception as e:
            text = f"An error occurred: {str(e)}"
            self.logger.error(e, exc_info=e)

        print(text)
        return text

    def get_token(self) -> str:
        """
        從 URL 中提取 token。

        :return: URL 中的 token。
        """
        token = self.url.split("/")[-1].split("?")[0]
        return token

    def check_visited(self) -> bool:
        """
        檢查當前 URL 的 token 是否已被訪問過。

        :return: 如果已訪問，則返回 True，否則返回 False。
        """
        visited_file = "visited.json"

        if not os.path.exists(visited_file):
            return False

        with open(visited_file, "r") as f:
            visited_data = json.load(f)

        token = self.get_token()

        return token in visited_data["visited"]

    def mark_visited(self):
        """
        將當前 URL 的 token 標記為已訪問。
        """
        visited_file = "visited.json"
        token = self.get_token()

        if os.path.exists(visited_file):
            with open(visited_file, "r") as f:
                visited_data = json.load(f)
        else:
            visited_data = {"visited": []}

        visited_data["visited"].append(token)

        with open(visited_file, "w") as f:
            json.dump(visited_data, f)

    def crawl_images(self):
        """
        爬取網站中的圖像 URL。
        """
        self.logger.info(self.url)
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tags = soup.find_all("img", class_="mimg")
        self.img_urls = [img["src"] for img in img_tags]
        self.img_prompt = img_tags[0]["alt"]
        self.trans_img_url_list()

    def get_image_urls(self) -> list:
        """
        獲取爬取的圖像原始縮圖 URL。

        :return: 爬取的圖像 URL 的列表。
        """
        return self.img_urls

    def get_trans_image_urls(self) -> list:
        """
        獲取爬取的圖像原始尺寸 URL。

        :return: 爬取的圖像 URL 的列表。
        """
        return self.trans_img_urls

    def trans_img_url_list(self):
        """
        轉換爬取的圖像原始原尺寸 URL。
        """
        for img_url in self.img_urls:
            trans_img_url = self.transform_url(img_url)
            self.logger.info(trans_img_url)
            self.trans_img_urls.append(trans_img_url)

    def transform_url(self, url: str) -> str:
        """
        將給定的網址轉換成指定的格式。

        :param url: 原始網址。
        :return: 轉換後的網址。
        """
        url_head, url_tail = url.split("/th/id/", 1)
        image_id, query_string = url_tail.split("?", 1)
        new_url = f"https://th.bing.com/th/id/{image_id}?pid=ImgGn"

        return new_url

    def download_images(self, folder=DEFAULT_FOLDER):
        """
        下載圖片到指定文件夾。(直接利用內部的self.trans_img_urls)
        :param folder: 圖片存儲文件夾。
        :return:
        """
        self._download_images(self.trans_img_urls, folder=folder)

    def _download_images(self, img_urls, folder=DEFAULT_FOLDER):
        """
        下載圖片到指定文件夾。

        :param img_urls: 要下載的圖片 URL 列表。
        :param folder: 圖片存儲文件夾。
        """
        if not folder:  # 若為空值，則儲存到預設資料夾img
            folder = DEFAULT_FOLDER
        if not os.path.exists(folder):
            os.makedirs(folder)

        for url in img_urls:
            response = requests.get(url)
            filename = self.img_prompt.split(".")[-1] + ".png"
            path = os.path.join(folder, filename)

            if os.path.exists(path):
                count = 1
                while True:
                    new_path = os.path.join(folder, "{} ({}).png".format(self.img_prompt.split(".")[-1], count))
                    if os.path.exists(new_path):
                        count += 1
                    else:
                        path = new_path
                        break
            with open(path, "wb") as f:
                f.write(response.content)
