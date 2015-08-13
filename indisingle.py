import sys, time, logging
import PyIndi

DEVICE_NAME = "SX CCD SuperStar"
 
class IndiClient(PyIndi.BaseClient):

    device = None

    def __init__(self):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('PyQtIndi.IndiClient')
        self.logger.info('creating an instance of PyQtIndi.IndiClient')
    def newDevice(self, d):
		#self.logger.info("new device " + d.getDeviceName())
		if d.getDeviceName() == DEVICE_NAME:
		    self.logger.info("Set new device %s!" % DEVICE_NAME)
		    # save reference to the device in member variable
		    self.device = d
    def newProperty(self, p):
		#self.logger.info("new property "+ p.getName() + " for device "+ p.getDeviceName())
		if self.device is not None and p.getName() == "CONNECTION" and p.getDeviceName() == self.device.getDeviceName():
		    self.logger.info("Got property CONNECTION for %s!" % DEVICE_NAME)
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
	self.logger.info("new BLOB "+ bp.name.decode())
	# get image data
	img = bp.getblobdata()
	import cStringIO
	# write image data to StringIO buffer
	blobfile = cStringIO.StringIO(img)
	# open a file and save buffer to disk
	with open("frame.fit", "wb") as f:
	    f.write(blobfile.getvalue())
	# start new exposure for timelapse images!
	# self.takeExposure()
	# disconnect from server
	self.disconnectServer()
    def newSwitch(self, svp):
        self.logger.info ("new Switch "+ svp.name.decode() + " for device "+ svp.device.decode())
    def newNumber(self, nvp):
        self.logger.info("new Number "+ nvp.name.decode() + " for device "+ nvp.device.decode())
    def newText(self, tvp):
        self.logger.info("new Text "+ tvp.name.decode() + " for device "+ tvp.device.decode())
    def newLight(self, lvp):
        self.logger.info("new Light "+ lvp.name.decode() + " for device "+ lvp.device.decode())
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
	exp[0].value = 0.01
	# send new exposure time to server/device
	self.sendNewNumber(exp)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

if __name__ == '__main__':
	# instantiate the client
	indiclient=IndiClient()
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