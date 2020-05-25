# RESTceiver

watch TV on your embedded device with a flask remote! 

---

## Installation

Requires
* ffmpeg
* vlc
* python3
* python3 flask

``` $ sudo apt-get install ffmpeg vlc ```

``` $ pip install -r requirements ```

Make sure, `cvlc` (vlc with dummy interface) is callable from shell (i.e. in `/bin/`) or set in `PATH` and you have a running internet connection.

You can make the app autostart on reboot by adding 

```@reboot /usr/bin/python3 /path/to/RESTceiver/main.py & ```

to `crontab -e`

## Usage

This code is intended to run on a device (e.g. a Raspberry Pi) attached to a TV screen, where there is no access to cable or DVB-T/DVB-S antennas, but broadband internet.
This device (playback device) will continuously play live TV streams (just like a SAT receiver) from the internet (HLS) and can be controlled by any other networked device, e.g. a smartphone to switch channels.

1. Connect the playback device to a display and the internet (use a wired connections for best stability)

1. Run the webserver on your playback device:

    ``` $ python3 main.py ```

1. Find the IP of your playback device, e.g. with

    ``` $ ifconfig ```

1. Open the remote control app on any other device in the local network by entering the playback device's IP address or mDNS host name into a web browser.

1. Switch channels by pressing on the corresponding buttons.

1. Get comfortable and enjoy the shows!

## Configuration

Channels are supplied in the [configuration file](config.json) with a name and their address. HTTP, RMTP, or anything else readable by ffmpeg will work.

## Known issues

* on some systems, when passing adaptive streaming m3u to the video player will not properly load video. Workaround: get an actual fixed quality stream and set it in the config by unpacking the playlist with

    ``` curl http://sometvstation/master.m3u8 ```

* switching channels takes a couple of seconds
* preview player is not killed automatically. [Possible solution](https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true)

## License notes

supplied TTF font: [inconsolata](https://www.levien.com/type/myfonts/inconsolata.html) by Raph Levien, published under the [SIL OPEN FONT LICENSE](LICENSE/OFL.txt)