try:
    from indiclient import IndiClient
except:
    print("INDiClient not installed")
import time, sys
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
from astropy.io import fits
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u
import numpy
from shutil import copyfile
import time
import json
from astroplan import Observer

FILENAME_FITS = 'latest.fits'
FILENAME_PNG = 'latest.png'
NIGHT_EXP  = 90
DAY_EXP = 0.00001
DATA_DIR = '/home/pi/images/'
resp = None


def take_exposure(exptime=DAY_EXP, filename=FILENAME_FITS):
    # instantiate the client
    indiclient=IndiClient(exptime, filename)
    # set indi server localhost and port 7624
    indiclient.setServer("localhost",7624)
    # connect to indi server pause for 2 seconds
    if (not(indiclient.connectServer())):
         print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
         return False
    time.sleep(1)

    # start endless loop, client works asynchron in background, loop stops after disconnect
    while indiclient.connected:
        time.sleep(1)
    return True

def set_exposure(brecon, currenttime):
    sunrise, sunset = rise_set(brecon, currenttime)
    exp = NIGHT_EXP
    print(sunrise, sunset, currenttime)
    if abs(sunrise - currenttime ) < timedelta(seconds=600) or abs(currenttime -sunset) < timedelta(seconds=600):
        exp = DAY_EXP
    elif abs(sunrise - currenttime) < timedelta(seconds=1800) or abs(currenttime -sunset) < timedelta(seconds=1800):
        exp = NIGHT_EXP/10.
    elif abs(sunrise - currenttime) < timedelta(seconds=5400) or (abs(currenttime -sunset) < timedelta(seconds=5400)):
        exp = NIGHT_EXP/2.
    print("Setting exposure time to %s (%s)" % (exp, sunrise-sunset))
    return exp

def setup():
    location = EarthLocation.from_geodetic(-3.48902*u.deg, 51.9249*u.deg, 300*u.m)
    brecon = Observer(location=location, name="Brecon", timezone="UTC")
    return brecon

def rise_set(brecon, currenttime):
    time = Time(currenttime)
    sunset_tonight = brecon.sun_set_time(time, which='nearest')
    sunrise_tonight = brecon.sun_rise_time(time, which='nearest')
    return (sunrise_tonight.datetime, sunset_tonight.datetime)


def make_image(fitsfile=FILENAME_FITS, pngfile=FILENAME_PNG):
    '''
    Function to read in the FITS file from Oculus.
    - find the 99.5% value
    - Make all values above 99.5% value white
    - Write image array to a PNG
    '''
    data = fits.getdata(fitsfile)
    #data1 = data.reshape(data.shape[0]*data.shape[1])
    max_val = numpy.percentile(data,99.5)
    scaled = data*256./max_val
    new_scaled = numpy.ma.masked_greater(scaled, 255.)
    new_scaled.fill_value=255.
    img_data = new_scaled.filled()
    result = Image.fromarray(img_data.astype(numpy.uint8))
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 24)
    textstamp = 'Brecon Beacons All Sky - %s' % datetime.now().strftime("%Y-%m-%d %H:%M")
    draw = ImageDraw.Draw(result)
    draw.text((10, 10), textstamp, font=font, fill=255)
    result.save(pngfile)
    return

def make_json(now=datetime.now()):
    nowtimestamp = datetime.strftime(now,"%a, %d %b %Y %H:%M:%S GMT+0000")
    latestdata = {'time' : nowtimestamp}
    latestjson = json.dumps(latestdata)
    filename = '%slatest.json' % (DATA_DIR)
    f = open(filename,'wb')
    f.write(latestjson)
    f.close()
    return



if __name__ == '__main__':
    brecon = setup()
    currenttime = datetime.utcnow()
    if brecon.is_night(currenttime):
        exp = set_exposure(brecon, currenttime)
        now = datetime.utcnow()
        datestamp = now.strftime("%Y%m%d-%H%M")
        fitsfile = '%s%s' % (DATA_DIR, FILENAME_FITS)
        pngfile = '%s%s.png' % (DATA_DIR, datestamp)
        latestpng = '%slatest.png' % (DATA_DIR)
        resp = take_exposure(exptime=exp, filename=fitsfile)
        if resp:
            make_image(fitsfile=fitsfile, pngfile=pngfile)
            copyfile(pngfile,latestpng)
            make_json(now)
            print("Saved %s - %s" % (pngfile, datetime.utcnow().isoformat()))
        else:
            print("Error!")
    else:
        print("Currently day - %s" % datetime.utcnow().isoformat())
