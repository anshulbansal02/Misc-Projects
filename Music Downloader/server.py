from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
import youtube_dl


API_KEY = "AIzaSyDheXlDNZHT7JJY2R2lqem7TKUVTh3XaPU"
search_endpoint = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video"
stats_endpoint = "https://www.googleapis.com/youtube/v3/videos?part=id%2C+statistics"



def downloadMusic(MusicId):
    downloadOptions = {
        'format': 'bestaudio/best'
    }


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])


def fetchResult(song):
    song = song.replace(" ", "+")

    response = requests.get(search_endpoint, params={
                            'q': song, 'key': API_KEY})

    searchList = response.json()

    idList = ""
    for item in searchList["items"]:
        id = item["id"]["videoId"]
        idList = idList + id + ","

    statsResponse = requests.get(stats_endpoint, params={
                                 'id': idList, 'key': API_KEY})
    statsResponse = statsResponse.json()

    statsList = []
    for item in statsResponse["items"]:
        statsList.append({"id": item["id"], "stats": item["statistics"]})
    
    resultList = []
    for item in searchList["items"]:
        
        id = item["id"]["videoId"]
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        description = item["snippet"]["description"]
        
        stats = list(filter(lambda i: i["id"] == id, statsList))[0]["stats"]

        stats['viewCount'] = human_format(int(stats['viewCount']))
        stats['likeCount'] = human_format(int(stats['likeCount']))
        stats['dislikeCount'] = human_format(int(stats['dislikeCount']))
        stats['commentCount'] = human_format(int(stats['commentCount']))

        resultList.append({
            "id": id,
            "thumbnail": thumbnail,
            "title": title,
            "channel": channel,
            "description": description,
            "stats": stats
        })



    return resultList

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=['POST'])
def search():

    songname = request.form['musicName']
    data = fetchResult(songname)
    return render_template("index.html", data=data)


@app.route("/download", methods=['POST'])
def download():
    downloadID = request.form['videoID']
    print("VIDEO ID: " + str(downloadID))
    return redirect('/')


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 405}), 405


if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0')



'''  Sample ResultList Item {
        "id": id,
        "thumbnail": thumbnail"
        "title": title,
        "channel": channel,
        "description": description,
        "stats": {
            "viewCount": "37773419",
            "likeCount": "867577",
            "dislikeCount": "15481",
            "favoriteCount": "0",
            "commentCount": "61251"
        }
    }
'''
