import sys, time, logging, io
import PyIndi

DEVICE_NAME = "SX CCD SuperStar"

class IndiClient(PyIndi.BaseClient):

    device = None

    def __init__(self, exptime=10.0, filename="frame.fits", device=DEVICE_NAME):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('PyQtIndi.IndiClient')
        self.logger.info('creating an instance of PyQtIndi.IndiClient')
        self.exptime = exptime
        self.filename = filename
        self.device = device
    def newDevice(self, d):
        #self.logger.info("new device " + d.getDeviceName())
        if d.getDeviceName() == self.device:
            self.logger.info("Set new device %s!" % self.device)
            # save reference to the device in member variable
            self.device = d
    def newProperty(self, p):
        if self.device is not None and p.getName() == "CONNECTION" and p.getDeviceName() == self.device.getDeviceName():
            self.logger.info("Got property CONNECTION for %s!" % self.device)
            # connect to device
            self.connectDevice(self.device.getDeviceName())
            # set BLOB mode to BLOB_ALSO
            self.setBLOBMode(1, self.device.getDeviceName(), None)
        if p.getName() == "CCD_EXPOSURE":
            # take first exposure
            self.takeExposure()
    def removeProperty(self, p):
        #self.logger.info("remove property "+ p.getName() + " for device "+ p.getDeviceName())
        pass
    def newBLOB(self, bp):
        self.logger.info("new BLOB "+ bp.name)
        # get image data
        img = bp.getblobdata()
        # write image data to StringIO buffer
        blobfile = io.BytesIO(img)
        # open a file and save buffer to disk
        with open(self.filename, "wb") as f:
            f.write(blobfile.getvalue())
        # start new exposure for timelapse images!
        # disconnect from server
        self.disconnectServer()
    def newSwitch(self, svp):
        self.logger.info ("new Switch "+ svp.name + " for device "+ svp.device)
    def newNumber(self, nvp):
        self.logger.info("new Number "+ nvp.name + " for device "+ nvp.device)
    def newText(self, tvp):
        self.logger.info("new Text "+ tvp.name + " for device "+ tvp.device)
    def newLight(self, lvp):
        self.logger.info("new Light "+ lvp.name + " for device "+ lvp.device)
    def newMessage(self, d, m):
        #self.logger.info("new Message "+ d.messageQueue(m).decode())
        pass
    def serverConnected(self):
        print("Server connected ("+self.getHost()+":"+str(self.getPort())+")")
        self.connected = True
    def serverDisconnected(self, code):
        self.logger.info("Server disconnected (exit code = "+str(code)+","+str(self.getHost())+":"+str(self.getPort())+")")
        # set connected to False
        self.connected = False
    def takeExposure(self):
        self.logger.info("<<<<<<<< Exposure >>>>>>>>>")
        #get current exposure time
        exp = self.device.getNumber("CCD_EXPOSURE")
        # set exposure time to 5 seconds
        exp[0].value = self.exptime
        # send new exposure time to server/device
        self.sendNewNumber(exp)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
