import configparser
import re
import subprocess

from neko import request
from neko import parser

config = configparser.ConfigParser()
config.read("config.ini")
url = config.get("Settings", "base_url")
user_agent = config.get("Settings", "user_agent")

html = request.Main(user_agent, url).get_html(url)
parser.Main().kominfo(html)
releases_list = parser.Main().get_release(html)

last_release_title, last_release_url, release_title, release_url = parser.Main().release_parse(releases_list[0])

print("New Release: " + str(last_release_title))
print("New Release Link: " + str(last_release_url))
print("Release: " + str(release_title))
print("Link: " + str(release_url))

release_html = request.Main(user_agent, url).get_html(last_release_url)
stream_url_1, stream_url_2 = parser.Main().stream_link(release_html)
print(stream_url_1)
print(stream_url_2)

stream2_html = request.Main(user_agent, url).get_html(stream_url_2)
stream = re.findall(r"(?!\'hls\': \')https:\/\/delivery-node.*(?=\',)", str(stream2_html))
print(stream[0])
subprocess.run("mpv " + "\"" + stream[0] + "\"", shell=True)
