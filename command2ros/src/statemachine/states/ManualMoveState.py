from states.State import State
from DataTransferProtocol import receiveData, sendData
from MovementData import MovementData
from ManualData import ManualData
from ScanData import ScanData
import socket
import time

class ManualMoveState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ManualMoveState", "ManualMoveState")
        self.HOST = "192.168.1.135"
        self.PORT = 20000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("attempt to connect manual")
        s.connect((self.HOST, self.PORT))
        print("connected manual")
        self.sock = s
        self.autonomousMode = False
        self.endProgram = False
        return

    #implementation for each state: overridden
    def run(self, cr, pub, scanID, moveID, megaProgress):           
        try:
            self.sock.setblocking(0) 
            sendData(self.sock, megaProgress)
            self.sock.setblocking(1)            
            manualCommand = receiveData(self.sock)
            print("received new command")            

            if manualCommand.endProgram:
                c = MovementData()
                c.endProgram = manualCommand.endProgram            
                cr.setCommand(c)                
                cr.sendCommand()  
                print("send command to end program")
                time.sleep(2)
                self.endProgram = True
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                print("manual state closed by end program")
            elif manualCommand.autonomousMode:
                self.autonomousMode = True
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                print("manual state closed by switch to autonomous")
            elif(manualCommand.forwardScan or manualCommand.backwardScan):
                if manualCommand.forwardScan:
                    pub.publish(scan=True, serialID=scanID)
                    print("Published command to scan forward")                    
                elif manualCommand.backwardScan:
                    pub.publish(scan=False, serialID=scanID) 
                    print("Published command to scan backwards")                    
                scanID += 1   
            else:
                c = MovementData()
                c.manualDrive = manualCommand.manualDrive
                c.manualTurn = manualCommand.manualTurn
                c.dig = manualCommand.dig
                c.dump = manualCommand.dump
                c.packin = manualCommand.packin
                c.cancel = manualCommand.stop
                c.serialID = moveID
                moveID += 1
            
                cr.setCommand(c)
                print("send movement command to robot")
                cr.sendCommand()                   
        except socket.error:
            c = MovementData()
            c.endProgram = True           
            cr.setCommand(c)                
            cr.sendCommand()  
            print("send command to end program")
            time.sleep(2)
            self.endProgram = True
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            print("manual state closed")
            print("Socket error manual command")     

        return (scanID, moveID)       
