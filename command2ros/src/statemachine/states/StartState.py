from states.State import State
from MovementData import MovementData
from LidarCommands import raspi_threads as rasp
from LidarCommands.constants import *

class StartState(State):
    def __init__(self):
        super().__init__("StartState", "ScanDigState")
        self.pub = None #publisher for scanning

    '''
    Run for StartState: Gets the robot ready to operate by unpacking the
            robot's wheels, scanning the environment, and moving the 
            robot to the front of the collection bin

    cr      CommandRobot allows commands to be published to the Mega
    scanID  ID number for the message to be published to the Scan topic
    moveID  ID number for the message to be published to the MovementCommand topic
    '''
    def run(self, cr, scanID, moveID):
        print("Start State: Unpack wheels")
        c = MovementData()
        c.serialID = moveID
        c.driveDist = 1
        moveID += 1
        cr.setCommand(c)        
        cr.sendCommand()

        print("Scan collection bin")
        scanID, z, distance = rasp.scan(self.pub, False, scanID)
        return (scanID, moveID)

    #keep copy of puublisher for scan topic
    def setPub(self, publisher):
        self.pub = publisher
