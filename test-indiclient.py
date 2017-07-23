import sys
import time
import logging

#import ctypes
#try:
#     ctypes.CDLL('libindi.so.0',  ctypes.RTLD_GLOBAL)
#except OSError:
#     print('libindi.so library not found. Please check the LD_LIBRARY_PATH environment variable')
#     print('   export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/path/to/libindi.so')
#     sys.exit(1)

import PyIndi
#import indiclientpython

def strISState(s):
    if (s == PyIndi.ISS_OFF):
        return "Off"
    else:
        return "On"

def strIPState(s):
    if (s == PyIndi.IPS_IDLE):
        return "Idle"
    elif (s == PyIndi.IPS_OK):
        return "Ok"
    elif (s == PyIndi.IPS_BUSY):
        return "Busy"
    elif (s == PyIndi.IPS_ALERT):
        return "Alert"

class IndiClient(PyIndi.BaseClient):
#class IndiClient(indiclientpython.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('PyQtIndi.IndiClient')
        self.logger.info('creating an instance of PyQtIndi.IndiClient')
    def newDevice(self, d):
        self.logger.info("new device " + d.getDeviceName())
        #self.logger.info("new device ")
    def newProperty(self, p):
        self.logger.info("new property "+ p.getName() + " for device "+ p.getDeviceName())
        #self.logger.info("new property ")
    def removeProperty(self, p):
        self.logger.info("remove property "+ p.getName() + " for device "+ p.getDeviceName())
    def newBLOB(self, bp):
        self.logger.info("new BLOB "+ bp.name.decode())
    def newSwitch(self, svp):
        self.logger.info ("new Switch "+ svp.name.decode() + " for device "+ svp.device.decode())
    def newNumber(self, nvp):
        self.logger.info("new Number "+ nvp.name.decode() + " for device "+ nvp.device.decode())
    def newText(self, tvp):
        self.logger.info("new Text "+ tvp.name.decode() + " for device "+ tvp.device.decode())
    def newLight(self, lvp):
        self.logger.info("new Light "+ lvp.name.decode() + " for device "+ lvp.device.decode())
    def newMessage(self, d, m):
        self.logger.info("new Message "+ d.messageQueue(m).decode())
    def serverConnected(self):
        print("Server connected ("+self.getHost()+":"+str(self.getPort())+")")
    def serverDisconnected(self, code):
        self.logger.info("Server disconnected (exit code = "+str(code)+","+str(self.getHost())+":"+str(self.getPort())+")")

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

indiclient=IndiClient()

indiclient.setServer("localhost",7624)

#test blob wrapping
#indiclient.connectServer()
#devccd=indiclient.getDevice('CCD Simulator')
#pccd=devccd.getProperty('CCD1')
#blobvccd=pccd.getBLOB()
#iblob=blobvccd[0]
#indiclient.setBLOBMode(1, 'CCD Simulator', 'CCD1')
#take an exposure
#img=iblob.getblobdata()
#import cStringIO
#blobfile=cStringIO.StringIO(img)
#import pyfits
#hdulist=pyfits.open(blobfile)
#hdulist.info()
# #Filename: <type 'cStringIO.StringI'>
# #No.    Name         Type      Cards   Dimensions   Format
# #0    PRIMARY     PrimaryHDU      20   (1280, 1024)   int16 
# #That rocks!! But not sure if image data won't break unicode/python string
#json transfer
#import base64
#img64=base64.b64encode(img)
#import json
#json.dumps(img64, cls=indi_echo_cherrypy_server.IndiJSONEncoder)

print("Connecting and waiting 2secs")
if (not(indiclient.connectServer())):
     print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
     print("  indiserver indi_simulator_telescope indi_simulator_ccd")
     sys.exit(1)
time.sleep(1)

print("List of devices")
dl=indiclient.getDevices()
for dev in dl:
    print(dev.getDeviceName())

print("List of Device Properties")
for d in dl:
    print("-- "+d.getDeviceName())
    lp=d.getProperties()
    for p in lp:
        print("   > "+p.getName())
        if p.getType()==PyIndi.INDI_TEXT:
            tpy=p.getText()
            for t in tpy:
                print("       "+t.name+"("+t.label+")= "+t.text)
        elif p.getType()==PyIndi.INDI_NUMBER:
            tpy=p.getNumber()
            for t in tpy:
                print("       "+t.name+"("+t.label+")= "+str(t.value))
        elif p.getType()==PyIndi.INDI_SWITCH:
            tpy=p.getSwitch()
            for t in tpy:
                print("       "+t.name+"("+t.label+")= "+strISState(t.s))
        elif p.getType()==PyIndi.INDI_LIGHT:
            tpy=p.getLight()
            for t in tpy:
                print("       "+t.name+"("+t.label+")= "+strIPState(t.s))
        elif p.getType()==PyIndi.INDI_BLOB:
            tpy=p.getBLOB()
            for t in tpy:
                print("       "+t.name+"("+t.label+")= <blob "+str(t.size)+" bytes>")

print("Disconnecting")
indiclient.disconnectServer()
