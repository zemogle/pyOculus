from indiclient import IndiClient
import time, sys
from datetime import datetime, timedelta
import ephem as eph
from PIL import Image
from astropy.io import fits
import numpy
from shutil import copyfile

FILENAME_FITS = 'latest.fits'
FILENAME_PNG = 'latest.png'
NIGHT_EXP  = 90
DAY_EXP = 0.01
DATA_DIR = '/home/pi/images/'


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
    sunset, sunrise = rise_set(currenttime)
    if (sunrise-sunset) < timedelta(days=1):
        exp = NIGHT_EXP
    else:
        exp = DAY_EXP
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
    data = fits.getdata(fitsfile)
    scaled = data*255./data.max()
    result = Image.fromarray(scaled.astype(numpy.uint8))
    result.save(pngfile)
    return



if __name__ == '__main__':
    currenttime = datetime.utcnow()
    exp = set_exposure(currenttime)
    datestamp = datetime.now().strftime("%Y%m%d-%H%M")
    fitsfile = '%s%s' % (DATA_DIR, FILENAME_FITS)
    pngfile = '%s%s.png' % (DATA_DIR, datestamp)
    latestpng = '%slatest.png' % (DATA_DIR)
    resp = take_exposure(exptime=exp, filename=fitsfile)
    if resp:
        make_image(fitsfile=fitsfile, pngfile=pngfile)
        copyfile(pngfile,latestpng)
        print("Saved %s" % pngfile)
