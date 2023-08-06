import configparser
import os
import re
import sys
import subprocess
import argparse

from neko import request
from neko import parsers


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", help="Print help trus exit")
parser.add_argument("-D", "--download", action="store_true", help="Download video.")
parser.add_argument("-d", "--directory", help="Ganti directory download.")
parser.add_argument("-s", "--search", help="Cari judul(bukan jodoh). -s, -C dan -J gak bisa digunain bareng. pilih satu")
parser.add_argument("-H", "--hentai", action="store_true", help="Hanya display kategori Hentai(default)")
parser.add_argument("-C", "--cg", action="store_true", help="Hanya display kategori Hentai 3D")
parser.add_argument("-J", "--jav", action="store_true", help="Hanya display kategori JAV")
args = parser.parse_args()


config = configparser.ConfigParser()
config.read("config.ini")
url = config.get("Settings", "base_url")
user_agent = config.get("Settings", "user_agent")

headers = {
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": url
        }

page = 1
if args.search and not args.cg and not args.jav:
    start_url = url + "search/" + args.search.replace(" ", "+")
elif args.cg and not args.search and not args.jav:
    start_url = url + "category/3d-hentai/"
elif args.jav and not args.cg and not args.search:
    start_url = url + "category/jav/"
elif not args.jav and not args.cg and not args.search:
    start_url = url + "category/hentai/"
else:
    print("Error. cek --help.")
    sys.exit(1)


html = request.Main().get_html(start_url, headers)
parsers.Main().kominfo(html)
releases_list = parsers.Main().get_release(html)
urls, titles = parsers.Main().release_parse(releases_list)


while True:
    print("Halaman " + str(page))
    for n, title in enumerate(titles):
        print(str(n + 1) + ". " + title)
    print("\nPilih Nomor Judul, Q buat keluar atau P/N buat pindah halaman: ", end="")
    answer = input()
    try:
        if int(answer) >= 1 and int(answer) - 1 <= n:
            title_num = int(answer) - 1
            break
        else:
            print("\nPilih Nomor Judul, Q buat keluar atau P/N buat pindah halaman: ", end="")
    except ValueError:
        if answer.lower() == "q" or answer.lower() == "quit" or answer.lower() == "exit":
            sys.exit(0)
        elif answer.lower() == "n" or answer.lower() == "next":
            if n < 9:
                print("Udah di halaman terakhir")
                continue
            page = page + 1
            page_url = start_url + "page/" + str(page) + "/"
            html = request.Main().get_html(page_url, headers)
            parsers.Main().kominfo(html)
            releases_list = parsers.Main().get_release(html)
            urls, titles = parsers.Main().release_parse(releases_list)
        elif answer.lower() == "p" or answer.lower() == "prev" or answer.lower() == "previous":
            if page <= 1:
                print("Udah di halaman pertama")
                continue
            page = page - 1
            if page == 1:
                page_url = start_url
            else:
                page_url = start_url + "page/" + str(page) + "/"
            html = request.Main().get_html(page_url, headers)
            parsers.Main().kominfo(html)
            releases_list = parsers.Main().get_release(html)
            urls, titles = parsers.Main().release_parse(releases_list)
        else:
            print("\rinput invalid.")

entry_url = urls[title_num]
print(entry_url)

release_html = request.Main().get_html(entry_url, headers)
stream_service_1, stream_service_2 = parsers.Main().stream_link(release_html, headers)
print(stream_service_2)

stream2_html = request.Main().get_html(stream_service_2, headers)
stream_url = re.findall(r"(?!\'hls\': \')https:\/\/delivery-node.*master\.m3u8.*(?=\',)", str(stream2_html))[0]
print(stream_url)

if args.download:
    ext_name = re.findall("(?<=master).*(?=\?t)", stream_url)
    if args.directory:
        directory = args.directory
    else:
        directory = ""
    request.Main().download(directory, titles[title_num], stream_url, headers)
else:
    subprocess.run("mpv " + "\"" + stream_url + "\"", shell=True)
