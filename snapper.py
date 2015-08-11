from indiclient import IndiClient
import time, sys
from datetime import datetime
import ephem as eph
import matplotlib as plt
from astropy.io import fits

FILENAME_FITS = 'latest.fits'
FILENAME_PNG = 'latest.png'
NIGHT_EXP  = 180
DAY_EXP = 0.01

  

def take_exposure(exptime=EXPTIME, filename=FILENAME):
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
    if sunset < currenttime and sunrise > currenttime:
        exp = NIGHT_EXP
    else:
        exp = DAY_EXP
    return exp


def rise_set(currenttime=None):
    brecon = eph.Observer()
    brecon.lat, brecon.lon = '51.924854', '-3.488342'
    brecon.date = currenttime.strftime('%Y/%m/%d %H:%M') if not currenttime else datetime.utcnow()
    sunrise_eph = brecon.previous_rising(eph.Sun()).tuple()
    sunset_eph = brecon.next_setting(eph.Sun()).tuple()
    sunrise = datetime(*sunrise_eph[0:-1])
    sunset = datetime(*sunset_eph[0:-1])
    return (sunrise, sunset)

def make_image(fitsfile=FILENAME_FITS, pngfile=FILENAME_PNG):
    data = fits.getdata(fitsfile)
    plt.imshow(data, cmap='gray', vmin=2.e3, vmax=15.e3)
    plt.savefig(pngfile,bbox_inches='tight', dpi=150)
    return



if __name__ == '__main__':
    currenttime = datetime.utcnow()
    exp = set_exposure(currenttime)
    datestamp = datetime.now().strftime("%Y%m%d-%H%M")
    fitsfile = '%s.fits' % datestamp
    pngfile = '%s.png' % datestamp
	resp = take_exposure(exptime=exp, filename=fitsfile)
    if resp:
        make_image(fitsfile, pngfile)
        print("Saved %s" % pngfile)
