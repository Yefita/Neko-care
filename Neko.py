import configparser
import os
import re
import sys
import subprocess
import argparse

from neko import request
from neko import parsers

def release_prompt(titles):
    for n, title in enumerate(titles):
        print(str(n + 1) + ". " + title)
    while True:
        print("\rPilih Judul: ", flush=True)
        answer = input()
        try:
            if int(answer) >= 1 and int(answer) - 1 <= n:
                title_num = int(answer) - 1
                return title_num
            else:
                print("\rpilih angka 1-" + str(n + 1) + ".")
        except ValueError:
            if answer.lower() == "q" or answer.lower() == "quit" or answer.lower() == "exit":
                sys.exit(0)
            else:
                print("\rinput invalid.")


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", help="Print help trus exit")
parser.add_argument("-D", "--download", action="store_true", help="Download video.")
parser.add_argument("--mp4", action="store_true", help="pake .mp4 format kalo ada.")
parser.add_argument("-d", "--directory", help="Ganti directory download.")
parser.add_argument("-s", "--search", help="Cari judul(bukan jodoh). -s, -C dan -J gak bisa digunain bareng. pilih satu")
parser.add_argument("-C", "--cg", action="store_true", help="Hanya display kategori Hentai 3D")
parser.add_argument("-J", "--jav", action="store_true", help="Hanya display kategori JAV")
args = parser.parse_args()


config = configparser.ConfigParser()
config.read("config.ini")
url = config.get("Settings", "base_url")
user_agent = config.get("Settings", "user_agent")

if args.search and not args.cg and not args.jav:
    url = url + "search/" + args.search.replace(" ", "+")
elif args.cg and not args.search and not args.jav:
    url = url + "category/3d-hentai/"
elif args.jav and not args.cg and not args.search:
    url = url + "category/jav/"
elif not args.jav and not args.cg and not args.search:
    url = url + "category/hentai/"
else:
    print("Error. cek --help.")
    sys.exit(1)


html = request.Main(user_agent, url).get_html(url)
parsers.Main().kominfo(html)
releases_list = parsers.Main().get_release(html)
urls, titles = parsers.Main().release_parse(releases_list)

entry_num = release_prompt(titles)
entry_url = urls[entry_num]

print("Release: " + str(titles[entry_num]))
print("Link: " + str(entry_url))

release_html = request.Main(user_agent, url).get_html(entry_url)
stream_service_1, stream_service_2 = parsers.Main().stream_link(release_html)
print(stream_service_1)
print(stream_service_2)

stream2_html = request.Main(user_agent, url).get_html(stream_service_2)
stream_mp4 = re.findall(r"(?!\'hls\': \')https:\/\/delivery-node.*master\.mp4.*(?=\',)", str(stream2_html))
stream_m3u8 = re.findall(r"(?!\'hls\': \')https:\/\/delivery-node.*master\.m3u8.*(?=\',)", str(stream2_html))

if args.mp4:
    try:
        stream_url = stream_mp4[0]
    except IndexError:
        print(".mp4 nggak ketemu. fallback ke .m3u8")
        stream_url = stream_m3u8[0]
else:
    stream_url = stream_m3u8[0]

if args.download:
    print(stream_url)
    ext_name = re.findall("(?<=master).*(?=\?t)", stream_url)
    name = release_title + ext_name[0]
    print(name)
    if args.directory:
        directory = args.directory
    else:
        directory = ""
    request.Main(user_agent, stream_url).download(directory, name, stream_url)
else:
    subprocess.run("mpv " + "\"" + stream_url + "\"", shell=True)
