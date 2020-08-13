from bs4 import BeautifulSoup
import requests
import time
from tabulate import tabulate
import re
from youtube_dl import YoutubeDL


"""
    Music Qualities/BitRates:
    1 - Low (128)
    2 - Ordinary (192)
    3 - Fine (256)
    4 - Superb (320)

    Video Qualities/Resolutions:
    1 - Full HD (1080)
    2 - HD (720)
    3 - Medium (480)
    4 - Low (360)
    5 - Very Low (240)

"""

verified = "✅"

def fetch_results(song, singer=""):
    base_url = "https://www.youtube.com/results?search_query="
    song = song.replace(" ", "+")
    singer = singer.replace(" ", "+")

    contents = requests.get(base_url + song + "+" + singer + "&sp=EgIQAQ%253D%253D").content
    page = BeautifulSoup(contents, 'html.parser')

    # Making a List of Results
    title, channel, length, u_date, view, url = [], [[], []], [], [], [], []

    # Collect All Search Items
    results = [d for d in page.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
    for item in results:

        # Make a list of all UserNames of all Channels
        if not item.find_all("a", href=re.compile(r"^/channel/")):
            channel[0].append(item.find_all("a", href=re.compile(r"^/user/")))
        else:
            channel[0].append(item.find_all("a", href=re.compile(r"^/channel/")))

        if item.find('span', {'class': "yt-channel-title-icon-verified"}) is None:
            channel[1].append(False)
        else:
            channel[1].append(True)

        # Make a list of all Titles of all Items
        title.append(item.find("a", {"class": "yt-uix-tile-link"}))

        # Make a list of Lengths of all Videos
        length.append(item.find("span", {"class": "video-time"}))

        # List upload dates and views of videos
        meta = item.find('div', {'class': "yt-lockup-meta"})
        for ul in meta:
            ul = BeautifulSoup(str(ul), 'html.parser')
            u_date.append(ul.select("ul > li:nth-of-type(1)"))
            view.append(ul.select("ul > li:nth-of-type(2)"))

        # Lists all the links to videos
        url.append(item.find('a', {'class': 'yt-uix-tile-link'})['href'])


    # Pass all the lists to combine_results
    param = [title, channel, length, u_date, view, url]
    return combine_results(*param)


def combine_results(ti, ch, ln, ud, vw, ul):
    results = [[], [[], []], [], [], [], []]

    # Append all the data into one table
    for i in range(20):
        title = ti[i].text
        title = re.sub(' +', ' ', title)
        title = title.replace("|", ",")
        title = title.replace("-", ",")
        title = title.replace(" ,", ",")

        if len(title) <=  45:
            short_title = title
        else:
            short_title = title[0:45] + "..."

        v = vw[i][0].text.replace(" views", "")
        v = v.replace(",", "")

        results[0].append(short_title)
        results[1][0].append(ch[0][i][0].text)
        results[1][1].append(ch[1][i])
        results[2].append(ln[i].text)
        results[3].append(v)
        results[4].append(ud[i][0].text)
        results[5].append(ul[i])

    return results

def best_choice(result):
    official = []
    views = []

    for i in range(len(result[3])):
        views.append(int(result[3][i]))
        official.append(result[1][1][i])

    pts = [0] * len(views)

    for i in range(len(pts)):
        for k in range(len(pts)-1):
            if views[i] > views[k+1]:
                pts[i] += 1

    for i in range(len(official)):
        if official[i]:
            pts[i] += 5


    return pts.index(max(pts))



# Display Organized results to Console
def display_results(result, start, stop):
    for i in range(start, stop):
        print("-" * 100)
        print(" | " + result[0][i] + "  [" + result[2][i] + "]")
        if result[1][1][i] == True:
            print(" || " + result[1][0][i] + " " + verified)
        else:
            print(" || " + result[1][0][i])

        views = result[3][i]

        if int(views) >= 1000000000:
            views = views[0:1] + "." + views[1:2] + "B"
        elif int(views) >= 100000000:
            views = views[0:3] + "M"
        elif int(views) >= 10000000:
            views = views[0:2] + "." + views[2:3] + "M"
        elif int(views) >= 1000000:
            views = views[0:1] + "." + views[1:2] + "M"
        elif int(views) >= 100000:
            views = views[0:3] + "K"
        elif int(views) >= 10000:
            views = views[0:2] + "." + views[2:3] + "K"
        elif int(views) >= 1000:
            views = views[0:1] + "." + views[1:2] + "K"


        print(" || " + result[4][i] + "\t || " + views)
        print("-"*100)



st = 0
stp = 5
tmp = 0

"""
while(True):
    if stp > 20:
        break
    print("Results (" + str(st) + "-" + str(stp) + "):")
    print(display_results(res, st, stp))
    print(":")
    q = input()
    if q == 'n':
        tmp = stp
        st = tmp
        stp = tmp + 5
        continue
"""



def auto_mode():
    print("|| Automatic Mode ||")

    """otg_opts = 'N'
    print("Enable OnTheGo Options? (Y/N): ")
    otg_opts = input()
    if otg_opts == 'Y' or otg_opts == 'y':
        print("Options Available:\n1) Quality\n2) Audio/Video\n3)")"""
    print("Enter Input File: ")
    input_file = input()
    print("Download Location: ")
    download_dir = input()
    print("Audio or Video? (A/V): ")
    type = input()
    if type == "V" or type == "v":
        print("Quality \n1) Full HD(1080)\n2) HD(720)\n3) Medium(480)\n4) Low(360)\n5) Very Low(240)\n: ")
        qlty = input()
    else:
        print("Quality (\n1) Superb(320)\n2) Fine(256)\n3) Ordinary(192)\n4) Low(128)\n: ")
        qlty = input()

    print("-"*30)
    print("Settings Overview:\nInput File: " + input_file + "\nDownload Directory: " + download_dir + "\nFile Type: " + type + "\nQuality: " + qlty)


    with open(input_file, 'r') as songs:
        song_list = songs.readlines()

    for song in song_list:
        result_songs = fetch_results(song)
        prime_song = best_choice(result_songs)
        print("Downloading " + result_songs[0][prime_song] + " by " + result_songs[1][0][prime_song] + "...")


auto_mode()

def semi_auto_mode():
    print("Semi-Automatic")


def manual_mode():
    print("Manual")





