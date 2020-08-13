from __future__ import unicode_literals
import time
import requests
import youtube_dl
from bs4 import BeautifulSoup

songs_list = []
completed_songs = []


with open('songs.txt') as music_file:
    for music in music_file:
        songs_list.append(music)



def song_list_search():




def search_music(song_name):
    song_name = song_name.replace(" ", "+")
    search_url = "https://www.youtube.com/results?search_query=" + song_name
    r = requests.get(search_url)
    page = BeautifulSoup(r.content, 'html5lib')




def download_music():
    pass

