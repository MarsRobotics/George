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
CommandRobot    Send robot movement commands to Arduino
"""
class CommandRobot:

    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 10000 
        self.lastData = MovementData()
        self.currentData = MovementData()        
        return
    
    #communication with the DataDistributor
    def sendCommand(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #connect to host
            s.connect((self.HOST,self.PORT))

            #receive last data sent
            try:
                receiveData(s)
            except socket.error:
                s.close()
                exit()

            #send new command data
            sendData(s, self.currentData)

    #assign a new command for the robot
    def setCommand(self, command):
        self.currentData.driveDist = command.driveDist
        self.currentData.turn = command.turn
        self.currentData.dig = command.dig
        self.currentData.dump = command.dump
        self.currentData.packin = command.packin
        self.currentData.eStop = command.eStop
        self.currentData.cancel = command.cancel
        self.currentData.pause = command.pause
        self.currentData.manualDrive = command.manualDrive
        self.currentData.manualTurn = command.manualTurn
        self.currentData.serialID = command.serialID

