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
        self.releases = html.find_all(class_="releases")
        self.new_releases = self.releases[1].parent
        self.releases_list = self.new_releases.find_all(class_="eroinfo")
        return self.releases_list

    def release_parse(self, release):
        self.entry = release.find_all("a", href=True)
        self.last_release_title = self.entry[0].text
        self.last_release_url = self.entry[0]["href"]
        self.release_title = self.entry[1].text
        self.release_url = self.entry[1]["href"]
        return self.last_release_title, self.last_release_url, self.release_title, self.release_url

    def stream_link(self, html):
        self.stream1 = html.find(id="stream1", class_="openstream").find("iframe")["src"]
        self.stream2 = html.find(id="stream2", class_="openstream").find("iframe")["src"]
        return self.stream1, self.stream2
