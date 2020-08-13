from flask import Flask, render_template, request, jsonify, redirect, url_for
import json



app = Flask(__name__)


@app.route("/")
def index():
    return render_template("queuepage.html")

@app.route("/songList", methods=["POST"])
def songList():
    text = request.form["songList"]
    songsL = text.splitlines()
    print(songsL)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")