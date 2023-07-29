import requests
from bs4 import BeautifulSoup

class Main:
    def __init__(self, user_agent, url):
        self.headers = {
            "User-Agent": user_agent,
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": url
            }

    def get_html(self, url):
        print(url)
        for i in range(5):
            try:
                self.result = requests.get(url, headers=self.headers)
                self.result = BeautifulSoup(self.result.text, "html.parser")
                return self.result
            except requests.exceptions.RequestException:
                continue
