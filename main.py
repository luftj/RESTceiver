#!/bin/python

import subprocess
from time import sleep
import json
from flask import Flask, render_template, request

app = Flask(__name__)
vlc_process = None

def get_stream_url(channel):
    with open("config.json") as urls_file:
        urls_json = json.load(urls_file)
        return urls_json[channel]

def get_stream_list():
    with open("config.json") as urls_file:
        urls_json = json.load(urls_file)
        result =  list(urls_json.keys())
        print(result)
        return result

@app.route('/')
def select():
    return render_template("channel_selector.html", channels = get_stream_list())

@app.route('/test',methods=["GET","POST"])
def test_run():
    global vlc_process
    if vlc_process:
        print("Kill!")
        vlc_process.kill()

    channel = request.form["channel"]
    channel = channel.lower()
    print("requested channel",channel)

    print("Running...")
    stream_url = get_stream_url(channel)
    vlc_process = subprocess.Popen(["cvlc", stream_url])
    print("wait...")
    return render_template("channel_selector.html", channels = get_stream_list())

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)