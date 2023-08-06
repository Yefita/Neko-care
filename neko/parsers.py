import sys
import re

from bs4 import BeautifulSoup
from neko import request

class Main():
    def kominfo(self, html):
        try:
            self.kominfo = html.find(class_="fw-bold mb-0").string
        except (TypeError, AttributeError):
            return
        if self.kominfo == "UNDANG-UNDANG NOMOR 19 TAHUN 2016 PASAL 40 (2a) dan (2b) TENTANG INFORMASI DAN TRANSAKSI ELEKTRONIK":
            print("Si kucing diblokir Kominfo. Coba lagi pakai DoH/DoT/VPN.\nkalo tetep gak bisa, open issue di github.")
            sys.exit(1)

    def get_release(self, html):
        self.releases = html.find(class_="result")
        self.releases_list = self.releases.find_all("li")
        return self.releases_list

    def release_parse(self, releases):
        self.urls = []
        self.titles = []
        for self.n, self.release, in enumerate(releases):
            self.entry = self.release.find("a", href=True)
            self.titles.append(self.entry.text)
            self.urls.append(self.entry["href"])
        return self.urls, self.titles

    def stream_link(self, html, headers):
        try:
            self.stream1 = html.find(id="stream1", class_="openstream").find("iframe")["src"]
            self.stream2 = html.find(id="stream2", class_="openstream").find("iframe")["src"]
            return self.stream1, self.stream2
        except AttributeError:
            self.episode_list = html.find(class_="episodelist").find_all("li")
            self.links = []
            self.episode_names = []
            for self.n, self.episode in enumerate(self.episode_list):
                self.links.append(self.episode.find("a", href=True)["href"])
                self.episode_names.append(self.episode.find("a", href=True).text)
            while True:
                self.answer = input("Pilih episode(1-" + str(self.n + 1) + "):")
                try:
                    for self.num, self.episode in enumerate(self.episode_names):
                        self.episode_num = re.sub(r'[^0-9.]', '', self.episode_names[self.num])
                        if float(self.answer) == float(self.episode_num):
                            print(self.links[self.num])
                            self.html = request.Main().get_html(self.links[self.num], headers)
                            self.stream1 = self.html.find(id="stream1", class_="openstream").find("iframe")["src"]
                            self.stream2 = self.html.find(id="stream2", class_="openstream").find("iframe")["src"]
                            return self.stream1, self.stream2
                except ValueError:
                    if self.answer.lower() == "q" or self.answer.lower() == "quit" or self.answer.lower() == "exit":
                        sys.exit(0)
                    elif self.answer.lower() == "l" or self.answer.lower() == "list":
                        for self.eps in self.episode_names:
                            print(self.eps)
