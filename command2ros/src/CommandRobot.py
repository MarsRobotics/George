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
        self.HOST = "192.168.1.45" #George
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
                receiveData(s)

                #send new data
                sendData(s, self.currentData)

