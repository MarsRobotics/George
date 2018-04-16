from states.State import State
#from states.MoveDigState import MoveDigState
from MovementData import MovementData
from LidarCommands import raspi_threads as rasp
from LidarCommands.constants import *

class ScanDigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ScanDigState", "MoveDigState")
        self.moveDigState = None
        self.digSiteDist = 5.67 #dump: 1.89m, obstacle: 3.78m, dig: 3.78m
        self.movedSoFar = 0.0
        self.pub = None

    def setPub(self, publisher):
        self.pub = publisher

    #implementation for each state: overridden
    def run(self, id):
        print("\n>run() not implemented\n")

        if self.movedSoFar >= self.digSiteDist:
            self.binCheck(id)

        moveCommand = MovementData()
        self.moveDigState.setNextMove(moveCommand)

        #thoughts: three threads- produce, consume, send data from LiDAR
        #use modified old code, for basics of plan see comments directly below

        #scan with LiDAR

        #A: create map for laptop
        #A: send map to laptop
        #A: receive move instructions from laptop

        #B: create map for AI
        #B: interpret map for AI & get move instructions

    def setMoveDig(self, digState):
        self.moveDigState = digState    

    def binCheck(self, id):        
        #tell motor to get into position and begin to move for scanning
        self.pub.publish(scan=False, serialID=id)                     
        print("Published command to scan backwards")   

        #begin scanning lidar
        distance, crossSection = rasp.scan() 
