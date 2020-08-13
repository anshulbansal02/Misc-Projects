import requests
from bs4 import BeautifulSoup

url = "https://www.saavn.com/s/playlist/anshulbansal104/Favourites_%F0%9F%8C%9F/rqjmefNXx7E_"
contents = requests.get(url).content
page = BeautifulSoup(contents, 'html.parser')


names = page.find_all('p', {'class': "song-name"})

song_list = []

for name in names:
    for child in name.find_all('p'):
        child.decompose()
    song_list.append(name.text)

with open('songs.txt', 'w') as sfile:
    for song in song_list:
        sfile.write(song + "\n")




