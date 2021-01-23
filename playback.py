#!/bin/python3
import math
import os

def mosaic(inputs, output_size, texts=None):
    command = "ffmpeg "
    for input_path in inputs:
        command += "-i \"%s\" " % input_path # supply all inputs

    command +=  "-filter_complex \"nullsrc=size=" # construct filter graph
    command += "%dx%d" % output_size # total size of output video
    command += "[tmp0];" # base target

    path = os.path.dirname(os.path.abspath(__file__))
    path += "/Inconsolata-Bold.ttf"
    font = "fontfile=%s" % path # get font. Shipped with repo for convenience
    part_size = (int(output_size[0] / math.ceil(len(inputs) / 2)), 
                 int(output_size[1] / math.floor(len(inputs) / 2))) # size for each subvideo

    for index,input in enumerate(inputs):
        command += "[%d:v] " % index # input target
        command += "setpts=PTS-STARTPTS, "
        command += "scale="+"x".join(map(str,part_size)) # target scale

        if texts:
            text = texts[index]
            command += ", drawtext=%s:fontcolor=white:fontsize=36:text=%s " % (font, text) # text overlay
        
        part_name = "tile%d" % index
        command += "[%s];" % part_name # output target
    
    numcols = math.ceil(len(inputs) / 2)
    for index,input in enumerate(inputs):
        part_name = "tile%d" % index
        x_offset = index % numcols
        y_offset = index // numcols
        video_x_pos = x_offset * part_size[0] # subvideo position in pixels (steps of subvideo size)
        video_y_pos = y_offset * part_size[1]

        command += "[tmp%d][%s] " % (index, part_name) # input target
        command += "overlay=" # overlay next video
        # command += "shortest=1:" # quit when first video quit
        command += "x=%d:y=%d " % (video_x_pos, video_y_pos) # subvieo x and y pos
        if index < len(inputs) - 1: # last subvideo doesn't have an output
            command += "[tmp%d]; " % (index+1) # output target
    command += "\" " # finish filter graph
    command += "-an " # no sound
    command += "-c:v libx264 -vcodec mpeg4 -f matroska - | ffplay -"
    return command

import json
configpath = os.path.dirname(os.path.abspath(__file__)) + "/config.json"

def get_stream_url(channel):
    with open(configpath) as urls_file:
        urls_json = json.load(urls_file)
        return urls_json[channel]

def get_stream_list():
    with open(configpath) as urls_file:
        urls_json = json.load(urls_file)
        result =  list(urls_json.keys())
        print(result)
        return result

def get_bitrate_stream(master_url, bitrate="lowest"):
    import requests
    r = requests.get(master_url)
    if r.status_code == 200:
        lines = r.text.split("\n")
        min_bandwith = [1000000000,""]
        for idx,line in enumerate(lines):
            if line.startswith("#EXT-X-STREAM-INF"):
                infos = line.split(",")
                bandwith = int([x for x in infos if ("BANDWIDTH") in x][0].split("=")[-1])
                if bandwith < min_bandwith[0]:
                    if lines[idx+1].startswith("http"):
                        url = (lines[idx+1])
                    else:
                        url = "".join(master_url.rsplit('/', 1)[0])
                        url += "/"+lines[idx+1]
                    min_bandwith = [bandwith, url]
        return min_bandwith
    else:
        print("error getting stream",r.status_code)
    
if __name__ == "__main__":
    inputs = ["https://brlive-lh.akamaihd.net/i/bralpha_germany@119899/index_6_av-p.m3u8?sd=10&rebase=on",
    "https://tagesschau-lh.akamaihd.net/i/tagesschau_3@66339/index_184_av-p.m3u8?sd=10&rebase=on",
    "https://zdfhls18-i.akamaihd.net/hls/live/744751/dach/1/1.m3u8",
    "https://artelive-lh.akamaihd.net/i/artelive_de@393591/index_5_av-p.m3u8?sd=10&rebase=on",
    "https://mcdn.daserste.de/daserste/de/master_184.m3u8"]
    texts = ["ard-alpha","tagesschau24","3sat","arte","ard"]
    output_size = (640,480)
    inputs = []
    for ch in get_stream_list():
        url = get_stream_url(ch)
        inputs.append(get_bitrate_stream(url)[1])
    print(*inputs,sep="\n")
    # command = mosaic(inputs,output_size,texts)
    # os.system(command)