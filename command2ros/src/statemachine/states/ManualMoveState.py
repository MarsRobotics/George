from states.State import State
from LidarCommands import raspi_threads as rasp
from LidarCommands.constants import *
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
        self.HOST = "192.168.1.136"
        self.PORT = 20000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("attempt to connect manual")
        s.connect((self.HOST, self.PORT))
        print("connected manual")
        self.sock = s
        self.autonomousMode = False
        self.endProgram = False
        self.distance = []
        self.crossSection = []
        return

    #implementation for each state: overridden
    def run(self, cr, pub, scanID, moveID):           
    #def run(self, pub, scanID, moveID):           
        try:
            self.sock.setblocking(1)            
            manualCommand = receiveData(self.sock)
            print("received new command")            

            if manualCommand.endProgram:
                c = MovementData()
                c.manual = True
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
                    #tell motor to get into position and begin to move for scanning
                    #pub.publish(scan=True, serialID=scanID)
                    #print("Published command to scan forward")  
                    
                    #begin scanning lidar
                    z, distance = rasp.scan(pub, True)  

                    if z != None:
                        print("distance")    
                        filename = "LiDAR_Scans/forward_LiDAR_distances_" + str(scanID) + ".txt"
                        with open(filename,"w") as f:
                            for d in distance:
                                p = str(d) + ", "
                                f.write(p)                            
                        print("done writing LiDAR data")
                elif manualCommand.backwardScan:
                    #tell motor to get into position and begin to move for scanning
                    #pub.publish(scan=False, serialID=scanID)                     
                    #print("Published command to scan backwards")   

                    #begin scanning lidar
                    z, distance = rasp.scan(pub, False)

                    if z != None:
                        print("distance")    
                        filename = "LiDAR_Scans/backwards_LiDAR_distances_" + str(scanID) + ".txt"
                        with open(filename,"w") as f:
                            for d in distance:
                                p = str(d) + ", "
                                f.write(p)                            
                        print("done writing LiDAR data")
                scanID += 1   
            else:                
                c = MovementData()
                c.manual = True    
                c.manualDrive = manualCommand.manualDrive
                c.manualTurn = manualCommand.manualTurn
                c.dig = manualCommand.dig
                c.dump = manualCommand.dump
                c.packin = manualCommand.packin
                c.cancel = manualCommand.stop
                c.serialID = moveID
                c.driveDist = manualCommand.drive
                c.turn = manualCommand.turn
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
