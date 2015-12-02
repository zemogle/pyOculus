from indiclient import IndiClient
import time, sys
from datetime import datetime, timedelta
import ephem as eph
from PIL import Image, ImageFont, ImageDraw
from astropy.io import fits
import numpy
from shutil import copyfile
from email import utils
import time
import json

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

def set_exposure(currenttime):
    sunrise, sunset = rise_set(currenttime)
    if (sunrise-sunset) < timedelta(days=1):
        exp = NIGHT_EXP
        if (sunrise - timedelta(seconds=5400)) < datetime.utcnow():
            exp = NIGHT_EXP/2.
        if (sunrise - timedelta(seconds=1800)) < datetime.utcnow():
            exp = NIGHT_EXP/10.
        if (sunrise - timedelta(seconds=600)) < datetime.utcnow():
            exp = DAY_EXP
    else:
        exp = DAY_EXP
    print("Setting exposure time to %s (%s)" % (exp, sunrise-sunset))
    return exp


def rise_set(currenttime=None):
    brecon = eph.Observer()
    brecon.lat, brecon.lon = '51.924854', '-3.488342'
    brecon.date = currenttime.strftime('%Y/%m/%d %H:%M') if not currenttime else datetime.utcnow()
    sunrise_eph = brecon.next_rising(eph.Sun()).tuple()
    sunset_eph = brecon.previous_setting(eph.Sun()).tuple()
    sunrise = datetime(*sunrise_eph[0:-1])
    sunset = datetime(*sunset_eph[0:-1])
    return (sunrise, sunset)

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
    font = ImageFont.truetype("FreeSans.ttf", 24)
    textstamp = 'Brecon Beacons All Sky - %s' % datetime.now().strftime("%Y-%m-%d %H:%M")
    draw = ImageDraw.Draw(result)
    draw.text((10, 10), textstamp, font=font, fill=255)
    result.save(pngfile)
    return

def make_json(now=datetime.now()):
    nowtuple = now.timetuple()
    nowtimestamp = time.mktime(nowtuple)
    latestdata = {'time' : utils.formatdate(nowtimestamp)}
    latestjson = json.dumps(latestdata)
    filename = '%slatest.json' % (DATA_DIR)
    f = open(filename,'wb')
    f.write(latestjson)
    f.close()
    return



if __name__ == '__main__':
    currenttime = datetime.utcnow()
    exp = set_exposure(currenttime)
    now = datetime.now()
    datestamp = now.strftime("%Y%m%d-%H%M")
    fitsfile = '%s%s' % (DATA_DIR, FILENAME_FITS)
    pngfile = '%s%s.png' % (DATA_DIR, datestamp)
    latestpng = '%slatest.png' % (DATA_DIR)
    if exp == NIGHT_EXP:
        resp = take_exposure(exptime=exp, filename=fitsfile)
        if resp:
            make_image(fitsfile=fitsfile, pngfile=pngfile)
            copyfile(pngfile,latestpng)
            make_json(now)
            print("Saved %s" % pngfile)
