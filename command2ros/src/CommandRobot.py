#!/usr/bin/env python3
# cPickle is faster
try:
    import cPickle as pickle
except ImportError:
    import pickle
    
import socket 
from socket import error as socketError
from MovementData import MovementData
from DataTransferProtocol import receiveData, sendData

BODY_SIZE_STRING_SIZE = 10

"""
CommandRobot    Send commands to Arduino through the DataServer
"""
class CommandRobot:

    def __init__(self):
        self.HOST = "127.0.0.1" #George
        self.PORT = 10000 #same port as DataDistributor
        self.lastData = MovementData()
        self.currentData = MovementData()
        return
    
    def createConnection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #connect to host
            s.connect((self.HOST,self.PORT))

            while True:
                #receive last data send
                try:
                    receiveData(s)
                except socket.error:
                    s.close()
                    exit()

                self.setMovementData()

                #send new data
                sendData(s, self.currentData)

    def setMovementData(self):
        self.currentData.driveDist = 10.5
        self.currentData.turn = 45        

