from states.State import State
from MovementData import MovementData
from LidarCommands import raspi_threads as rasp
from LidarCommands.constants import *

class ScanDumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ScanDumpState", "MoveDumpState")
        self.moveDumpState = None
        self.maxBinDist = 4 #inches
        self.distFromBin = 0.0
        self.pub = None

    def setPub(self, publisher):
        self.pub = publisher

    '''
    Run for ScanDumpState:  Scan the environment for the collection bin and 
                create path towards the collection bin, moving around 
                obstacles. When the robot is within the maxBinDist range,
                set the next transition to the DockingBinState.

    cr      CommandRobot allows commands to be published to the Mega
    scanID  ID number for the message to be published to the Scan topic
    moveID  ID number for the message to be published to the MovementCommand topic
    '''
    def run(self, cr, scanID, moveID):    
        self.nextState = "MoveDumpState"
        if self.distFromBin <= maxBinDist:
            self.binCheck(scanID)

        moveCommand = MovementData()
        self.moveDumpState.setNextMove(moveCommand)

        return (scanID+1, moveID)

    #keep MoveDumpState to update movement commands
    def setMoveDump(self, dumpState):
        self.moveDumpState = dumpState

    #check if the robot is close enough to begin docking
    def binCheck(self, id):        
        crossSection, distance = rasp.scan(self.pub, True, id) 
        #set next state to "DockingBinState" if close enough
