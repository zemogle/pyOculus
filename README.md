# pyOculus
Python set up for Oculus allsky camera on Raspberry Pi. The code is currently running on an Starlight Xpress Oculus installed in the [Brecon Beacons National Park](http://www.breconbeacons.org/national-park-visitor-centre), in South Wales. More details about the installation are on my blog, [Dark Matter Sheep](http://darkmattersheep.uk/blog/brecon-allsky/).

## Setup
- A Raspberry Pi
- Need to install [INDI server](http://indilib.org/download/category/6-raspberry-pi.html) for Raspberry Pi.
- Install Swig via `sudo apt-get install swig` you may need to do `sudo apt-get install -f` to get the dependencies
- You may also need to install python dev using `sudo apt-get install python-dev`
- I recommend doing this inside a `virtualenv` or a `conda` environment, to prevent funny stuff with permissions.
- Install the [PyINDI client] by doing
```bash
pip3 install pyindi-client
```
- Note: This code now uses Python 3. If you need a code using Python 2, [use the V1.0 release](https://github.com/zemogle/pyOculus/archive/v1.0.zip).
- I use `s3cmd` to transfer the images to Amazon S3 but you could copy them to any other location off the Pi.

You should already have `python` and `git` if you are using Raspbian.

[OPTIONAL INSTALLS]
- I use ImageMagick (for JPEG compression) and FFMPEG for making the video of the timelapse
You will have to add the following to your `/etc/apt/sources.list` to get ffmpeg
'''bash
deb http://ftp.uk.debian.org/debian jessie-backports main
'''
Then running following should install ffmpeg and ImageMagick fine.
'''bash
sudo apt-get update
sudo apt-get install ffmpeg
sudo apt-get install imagemagick
'''


## Instructions
The INDI server handles all the communication with the camera, so the server has to be running for this code to be able to talk to the camera. In my case Oculus uses a Starlight Xpress CCD, so I started the camera with:

`indiserver -v -m 100 indi_sx_ccd`

This needs to be running when you do the next step, so open a new terminal (or if you are running headless, open another ssh session).

`python snapper.py --test`

will save a file called `latest.fits` after taking an image.

## Testing Setup

If you are in doubt of whether the camera is connected and working, you can run the following test script (assuming the INDi server is running):

`python pyOculus/test-indiclient.py`
