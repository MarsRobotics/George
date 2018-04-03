#!/usr/bin/env python3
# cPickle is faster
try:
    import cPickle as pickle
except ImportError:
    import pickle
    
import time
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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        self.sock = s
        self.lastData = MovementData()
        self.currentData = MovementData() 
        return

    def stop(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        print("command robot is closed")

    #communication with the DataDistributor
    def sendCommand(self):        
        #send new command data
        sendData(self.sock, self.currentData)
        time.sleep(2)
        if self.currentData.endProgram:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            print("command robot is closed")

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
        self.currentData.endProgram = command.endProgram

