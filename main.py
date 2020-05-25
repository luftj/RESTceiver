#!/bin/python3

import subprocess
from time import sleep
import json
from flask import Flask, render_template, request
from playback import * 

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
def root():
    return render_template("channel_selector.html", channels = get_stream_list())

@app.route('/select',methods=["GET","POST"])
def select():
    global vlc_process
    if vlc_process:
        print("Kill!")
        vlc_process.kill()

    channel = request.form["channel"]
    channel = channel.lower()
    print("requested channel",channel)

    print("Running...")
    stream_url = get_stream_url(channel)
    vlc_process = subprocess.Popen(["cvlc", "--fullscreen", stream_url])
    print("wait...")
    return render_template("channel_selector.html", channels = get_stream_list())

@app.route("/preview")
def preview():
    print("preview")
    global vlc_process
    if vlc_process:
        print("Kill!")
        vlc_process.kill()
    print("Run preview")
    texts = get_stream_list()
    inputs = [get_stream_url(ch) for ch in texts]
    output_size = (1920,1080)
    command = mosaic(inputs,output_size,texts)
    vlc_process = subprocess.Popen(command, shell=True)

    return render_template("channel_selector.html", channels = get_stream_list())

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)