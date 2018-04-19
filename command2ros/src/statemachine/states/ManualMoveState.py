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
        self.HOST = "192.168.1.137"         #laptop IP
        self.PORT = 20000                   #communication port

        #connect to laptop (note: laptop program is server so must start laptop program first)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("attempt to connect manual")
        s.connect((self.HOST, self.PORT))
        print("connected manual")
        self.sock = s
        self.autonomousMode = False
        self.endProgram = False
        self.pub = None         #publisher for the Scan topic
        return

    '''
    Run for ManualMoveState:    Receive manual commands to direct robot from a laptop

    cr      CommandRobot allows commands to be published to the Mega
    scanID  ID number for the message to be published to the Scan topic
    moveID  ID number for the message to be published to the MovementCommand topic
    '''
    def run(self, cr, scanID, moveID):              
        try:
            self.sock.setblocking(1)            
            manualCommand = receiveData(self.sock)
            print("received new command")            

            #shut down the robot
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
            #switch to autonomous mode
            elif manualCommand.autonomousMode:
                self.autonomousMode = True
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                print("manual state closed by switch to autonomous")
            #scan LiDAR
            elif(manualCommand.forwardScan or manualCommand.backwardScan):
                if manualCommand.forwardScan:
                    #tell motor to get into position and begin to move for scanning   
                    scanID, z, distance = rasp.scan(self.pub, True, scanID)  

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
                    scanID, z, distance = rasp.scan(self.pub, False, scanID)

                    if z != None:
                        print("distance")    
                        filename = "LiDAR_Scans/backwards_LiDAR_distances_" + str(scanID) + ".txt"
                        with open(filename,"w") as f:
                            for d in distance:
                                p = str(d) + ", "
                                f.write(p)                            
                        print("done writing LiDAR data")
                scanID += 1   
            #command robot to move
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
        #socket was shut down unexpectedly, shut down robot                         
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

    #keep publisher for Scan topic
    def setPub(self, publisher):
        self.pub = publisher   
