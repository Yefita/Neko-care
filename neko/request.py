import requests
import youtube_dl
import sys
import os
from bs4 import BeautifulSoup

class Main:
    def get_html(self, url, headers):
        for i in range(10):
            try:
                print("request")
                self.result = requests.get(url, headers=headers)
                self.result = BeautifulSoup(self.result.text, "html.parser")
                if self.result == None:
                    continue
                return self.result
            except requests.exceptions.RequestException:
                continue
        if i <= 10:
            print("Request gagal, cek koneksi internet")
            sys.exit(1)

    def download(self, directory, name, url, headers):
        self.options = {
                "outtmpl": os.path.join(directory, name),
                "nocheckcertificate": True,
                "disabledebug": True
                }
        with youtube_dl.YoutubeDL(self.options) as ytdl:
            ytdl.download([url])

