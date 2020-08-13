from bs4 import BeautifulSoup
import requests
import time
import re
import youtube_dl
import eyed3
import os

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
    results = [[], [[], []], [], [], [], [], []]

    # Append all the data into one table
    for i in range(20):
        title = ti[i].text

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
        results[6].append(ti[i].text)

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


def download(url, dir):
    url = "https://www.youtube.com" + url

    opts = {
        'outtmpl': dir + '%(title)s.%(ext)s',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
        'nocheckcertificate': True,
        'quiet': True,
        'writethumbnail': True,
        'no_warnings': True
    }

    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])






print("Songs List: ", end='')
songs_file = input()



with open(songs_file, 'r') as songs:
    song_list = songs.readlines()

no_of_vid = len(song_list)
print("Download Directory: ", end='')
loc = input()
print("\n" + "-"*30 + " Download Starting " + "-"*30)


info_opts = {
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True
    }



def update_meta(path):
    path = "C:\\Users\\Anshul\\PycharmProjects\\MusicWiz" + path
    song_path = path + ".mp3"
    img_path = path + ".jpg"

    song = eyed3.load(song_path)

    if (song.tag == None):
        song.initTag()

    song.tag.images.set(3, open(img_path, 'rb').read(), 'image/jpeg')
    song.tag.save()
    os.remove(img_path)




playlist_start = time.time()
count = 1
for song in song_list:
    start = time.time()

    results = fetch_results(song)
    best_song = best_choice(results)

    prime_song_url = results[5][best_song]
    print("Song [" + str(count) + " of " + str(no_of_vid) + "]")
    count += 1
    print("Downloading " + results[0][best_song])
    download(prime_song_url, loc)
    time_elapsed = time.time() - start
    time_elapsed_min = int(time_elapsed / 60)
    time_elapsed_sec = int(time_elapsed % 60)
    update_meta(loc + str(results[6][best_song]))
    print(" - Downloaded in " + str(time_elapsed_min) + " m " + str(time_elapsed_sec) + " s")
    print("-"*80)


playlist_time = time.time() - playlist_start
time_elapsed_min = int(playlist_time / 60)
time_elapsed_sec = int(playlist_time % 60)
print("-"*80 + "\nAll Songs Downloaded in " + str(time_elapsed_min) + " m " + str(time_elapsed_sec) + " s\n" + "-"*80)



