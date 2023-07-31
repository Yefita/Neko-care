import requests
import sys
from bs4 import BeautifulSoup

class Main:
    def __init__(self, user_agent, url):
        self.headers = {
            "User-Agent": user_agent,
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": url
            }

    def get_html(self, url):
        for i in range(10):
            try:
                print("request")
                self.result = requests.get(url, headers=self.headers)
                self.result = BeautifulSoup(self.result.text, "html.parser")
                if self.result == None:
                    continue
                return self.result
            except requests.exceptions.RequestException:
                continue
        if i <= 9:
            print("Request gagal, cek koneksi internet")
            sys.exit(1)

    def download(self, directory, name, url):
        self.response = requests.get(url, stream=True, headers=self.headers)
        with open(os.path.join(directory, name), "wb") as file:
            for data in self.response.iter_content(chunk_size=512):
                file.write(data)

