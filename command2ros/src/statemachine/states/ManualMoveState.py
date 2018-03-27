from states.State import State
from DataTransferProtocol import receiveData
import socket

class ManualMoveState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ManualMoveState", "ManualMoveState")
        self.HOST = "192.168.1.2"
        self.PORT = 20000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("attempt to connect manual")
        s.connect((self.HOST, self.PORT))
        print("connected manual")
        self.sock = s
        return

    #implementation for each state: overridden
    def run(self, cr):           
        try:
            self.sock.setblocking(0)
            print("attempt to receive new command")
            newCommand = receiveData(self.sock)
            print("received new command")
            cr.setCommand(newCommand)
        except socket.error:
            print("Socket error manual command")
