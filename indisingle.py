import sys, time, logging
import PyIndi
from indiclient import IndiClient

DEVICE_NAME = "SX CCD SuperStar"

if __name__ == '__main__':
	# instantiate the client
	indiclient=IndiClient(10.0,'test.fits',DEVICE_NAME)
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
