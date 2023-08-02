import sys
import re

from bs4 import BeautifulSoup

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

    def stream_link(self, html):
        self.stream1 = html.find(id="stream1", class_="openstream").find("iframe")["src"]
        self.stream2 = html.find(id="stream2", class_="openstream").find("iframe")["src"]
        return self.stream1, self.stream2
