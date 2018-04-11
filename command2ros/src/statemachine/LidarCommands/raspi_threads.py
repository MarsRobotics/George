
__author__="Jaimiey Sears, updated by Alex Schendel and Alex Reinemann, 2018"
__copyright__="October 26, 2015"
__version__= 0.50

import queue
import threading
import socket
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from LidarCommands.utility import *
from LidarCommands.constants import *
import pickle
import time
#from time import sleep

##############################
#  PROGRAM MAIN ENTRY POINT  #
##############################
def scan():
    lt = LidarThreads(debug=False)

    # make the first thread for reading LIDAR data
    debugPrint("Starting", ROSTA)
    th1_stop = threading.Event()
    th1 = threading.Thread(target=lt.produce, args=(lt.dataQueue, th1_stop,), name="data_reader")
    debugPrint("Done making thread 1", ROSTA)

    # make the second thread to process the LIDAR data
    th2_stop = threading.Event()
    th2 = threading.Thread(target=lt.consume, args=(lt.dataQueue, th2_stop,), name="cartesian_converter")
    debugPrint("done making thread 2", ROSTA)

    # start both threads
    th1.start()
    th2.start()

    # close the threads down
    while th1.isAlive():
        # th1_stop.set()
        th1.join(1.0)

    debugPrint("producer stopped", ROSTA)

    while th2.isAlive():
        th2_stop.set()
        th2.join(1.0)

    debugPrint("consumer stopped", ROSTA)

    th1_stop.set()
    th2_stop.set()

    x = np.asarray(lt.processedDataArrays[0])
    y = np.asarray(lt.processedDataArrays[1])
    z = np.asarray(lt.processedDataArrays[2])
    #plt.pcolormesh([z, lt.processedDataArrays[5]])  # Figure out how this works! Also, why z and dist
    #plt.colorbar()  # need a colorbar to show the intensity scale
    #plt.show()

    return lt.processedDataArrays[2], lt.processedDataArrays[5]
    debugPrint("Done running threads", ROSTA)
    debugPrint("exiting with code {}".format(lt.exit()), ROSTA)
    debugPrint("queue size at exit: {}".format(lt.dataQueue.qsize()), ROSTA)
    raise SystemExit
#####################
## UNIT TEST 1 END ##
#####################



##
# LidarThreads
# class controls threads for gathering LIDAR data
# **Version 0.10 the actual functions are simulated with time.sleep statements**
##
class LidarThreads():
    def __init__(self, debug=False):
        # don't forget: netsh interface ip set address "Local Area Connection" static 192.168.0.100
        global nhokreadings

        # controls a number of debug statements which should only print sometimes
        self.debug = debug

        self.commandOutput = ""
        self.dataOutput = ""

        self.slitAngle = START_ANGLE

        #command to get data from the lidar.
        #MD=Distance measurement with continuous scanning
        #Parameters:
        #Position at the starting step, length 4, name:Start. 
        #Position at the ending step, length 4, name:End.Units unknown
        #Number of group steps, length 2, name:Grouping Units unknown
        #Number of scans to skip, length 1, name:Skips
        #Number of measurement scans, length 2, name:Scans
        #Documentation: https://en.manu-systems.com/HOK-UTM-30LX-EW_communication_protocol.pdf
        strcommand = 'MD'+'0000'+'1000'+'00'+'0'+'00'+'\n'
        self.command=bytes(strcommand, 'ascii')#convert to ascii encoded binary
        # establish communication with the sensor.
        # NOTE, special network settings are required to connect:
        # IP: 192.168.1.11, Subnet Mask: 255.255.255.0 (default) Default Gateway: 192.168.0.1
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.settimeout(.1)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.socket.connect(("192.168.0.10", 10940))
        except socket.timeout as e:
            debugPrint("I can't connect. Exiting.", SOCKET_MSG)
            exit(-1)

        # dataQueue is a Queue of strings
        # each string representing a slice (scan)
        self.dataQueue = queue.Queue()

        self.processedDataArrays = []

    ##
    # produce
    #
    # Description: gets data from the LIDAR unit, puts it into the queue
    #
    # Parameters:
    #   dataQueue - queue to submit data to
    #   stop_event - event to listen to for exit
    ##
    def produce(self, dataQueue, stop_event):
        counter = 0
        angle = -1
        for i in range (0,2):#number of slices to scan along y-axis (moving servo motor)

                # wait for the Queue to empty
                while dataQueue.qsize() > 0:
                  pass
                angle = angle+1
                # get the starting theta angle
                self.slitAngle = START_ANGLE

                # get data from the user
                # print "\n>>> Rotate LiDAR to {} degrees".format(ang)
                # inp = raw_input(">>> Press enter when ready to make a scan\n")
                # if inp == "":
                start = time.time()
                # send scan request to the LIDAR
                self.socket.sendall(self.command)
                end = time.time()
                debugPrint("Time difference: {}".format(end-start), ROSTA)
                #astr ='MD'+'0180'+'0900'+'00'+'0'+'01'+'\n'
                #self.socket.sendall(astr.encode())
                #sleep(0.1)
                debugPrint("Scanning angle...\n", SOCKET_DATA)
                # receive data from the LIDAR
                for j in range(0, 90):#number of slices to scan along x-axis (resolution)
                    try:
                        temp = self.socket.recv(4500)#receive up to 4500 bytes of data
                        #debugPrint("Recv:\n" + temp.decode()[:8], SOCKET_DATA)
                        data = temp.decode().split("\n")#decode the data and split it by new line
                        data.reverse()
                    except socket.timeout as e:
                        debugPrint("waiting for data", SOCKET_MSG)
                        break
                    

                    while data:
                        try:
                            str = data.pop()
                            # put data into our queue for the consumer to use
                            dataQueue.put((str, angle))

                        except queue.Full as e:
                            debugPrint("Data Queue is full.", SOCKET_MSG)
                            continue
                    counter += 1.0

    ##
    # consume
    #
    # Description: consumes data from the queue
    #
    # Parameters:
    #   dataQueue - queue to consume from
    #   stop_event - the event to watch for quitting.
    ##
    def consume(self, dataQueue, stop_event):
        counter = 0
        xLines = []
        yLines = []
        zLines = []
        phiLines = []
        thetaLines = []
        distLines = []
        timeLines = []

        dataSet = ""
        currTime = None
        emptied = False
		
        index = 0

        while not stop_event.is_set():

            try:
                # get some data from the queue, process it to cartesian
                dataline, anglePhi = dataQueue.get(timeout=0.25)
                emptied = False

                if dataline == "":
                    if not dataSet == "":
                        for string in splitNparts(dataSet,64):
                            X, Y, Z, dist, phi, th = decode_new(string, anglePhi)

                            #self.slitAngle = lastAngle

                            xLines = xLines + X
                            yLines = yLines + Y
                            zLines = zLines + Z
                            phiLines = phiLines + phi
                            thetaLines = thetaLines + th
                            distLines = distLines + dist
                            # timeLines = timeLines + currTime
                            #debugPrint(str(distLines), SOCKET_DATA)

                    dataSet = ""
                    continue
                elif dataline == self.command:
                    counter = 0
                else:
                    counter += 1

                #debugPrint("Consumer: data= {}".format(dataline), SOCKET_DATA)

                self.commandOutput += dataline + '\n'
                # if counter == 4:
                #     currTime = [decodeShort(dataline[:-1])]
                if counter >= 5:
                    dataSet = dataSet + dataline

            except queue.Empty as e:
                if not emptied:
                    debugPrint( "Data Queue is empty", SOCKET_MSG)
                    emptied = True
                continue

        self.processedDataArrays = (xLines, yLines, zLines, phiLines, thetaLines, distLines)

    ##
    # exit
    #
    # Description: closes out the socket
    # returns: 0 on success, -1 on failure
    ##
    def exit(self):
        if not self.socket is None:
            self.socket.close()
            return 0
        else:
            return -1
