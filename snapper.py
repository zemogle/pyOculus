from indiclient import IndiClient
import time, sys
from datetime import datetime
import ephem as eph

FILENAME = 'latest.fits'
NIGHT_EXP  = 180
DAY_EXP = 0.01

  

def take_exposure(exptime=EXPTIME, filename=FILENAME):
    # instantiate the client
    indiclient=IndiClient(exptime, filename)
    # set indi server localhost and port 7624
    indiclient.setServer("localhost",7624)
    # connect to indi server
    print("Connecting and waiting 2secs")
    if (not(indiclient.connectServer())):
         print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
         print("  indiserver indi_simulator_telescope indi_simulator_ccd")
         sys.exit(1)
    time.sleep(1)
     
    # start endless loop, client works asynchron in background, loop stops after disconnect
    while indiclient.connected:
        time.sleep(1)

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

if __name__ == '__main__':
    currenttime = datetime.utcnow()
    exp = set_exposure(currenttime)
	take_exposure(exptime=exp)