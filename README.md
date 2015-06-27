# pyOculus
Python set up for Oculus allsky camera on Raspberry Pi

## Setup
- Need to install [INDI server](http://indilib.org/download/category/6-raspberry-pi.html) for Raspberry Pi.
- Install Swig via `sudo apt-get install swig` you may need to do `sudo apt-get install -f` to get the dependencies
- You may need to install `cmake` with `sudo apt-get install cmake` before the next step
- Install the [PyINDI client](https://github.com/zemogle/pyindi-client) by doing
`
mkdir libindipython
cd libindipython
cmake ../pyindi-client/swig-indi/swig-indi-python
make
sudo make install
`

You should already have `python` and `git` if you are using Raspbian.

## Instructions
The INDI server handles all the communication with the camera, so the server has to be running for this code to be able to talk to the camera. In my case Oculus uses a Starlight Xpress CCD, so I started the camera with:

`indiserver -v -m 100 indi_sx_ccd`

This needs to be running when you do the next step, so open a new terminal (or if you are running headless, open another ssh session).

`python indi_single.py`

will save a file called `frame.fits` after taking a 1s image.

