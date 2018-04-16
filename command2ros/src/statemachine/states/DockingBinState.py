from states.State import State
from MovementData import MovementData
from LidarCommands import raspi_threads as rasp
from LidarCommands.constants import *

class DockingBinState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("DockingBinState", "DumpState")
        self.pub = None

    '''
    Run for DockingBinState:    Dock the robot to the collection bin for 
            depositing the icy regolith.

    cr      CommandRobot allows commands to be published to the Mega
    scanID  ID number for the message to be published to the Scan topic
    moveID  ID number for the message to be published to the MovementCommand topic
    '''
    def run(self, cr, scanID, moveID):
        print("Turn robot around to back into collection bin")
        c = MovementData()
        c.serialID = moveID
        moveID += 1
        c.turn = 180
        cr.setCommand(c)
        cr.sendCommand()

        crossSection, distance = rasp.scan(self.pub, False, scanID)
        scanID += 1

        return (scanID, moveID)

    #keep copy of publisher to Scan topic
    def setPub(self, publisher):
        self.pub = publisher 