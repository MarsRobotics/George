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

    #implementation for each state: overridden
    def run(self, id):    
        if self.distFromBin <= maxBinDist:
            self.binCheck(id)

        moveCommand = MovementData()
        self.moveDumpState.setNextMove(moveCommand)

    def setMoveDump(self, dumpState):
        self.moveDumpState = dumpState

    def binCheck(self, id):        
        #tell motor to get into position and begin to move for scanning
        self.pub.publish(scan=True, serialID=id)                     
        print("Published command to scan forwards")   

        #begin scanning lidar
        distance, crossSection = rasp.scan() 
