from states.State import State
from states.MoveDigState import MoveDigState
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

    '''
    Run for ScanDigState: Scan the environment to move the robot to the 
            excavation site, avoid obstacles. When the robot is past the 
            digSiteDist then check that the robot is in the excavation
            site and set the next transition for the DigState

    cr      CommandRobot allows commands to be published to the Mega
    scanID  ID number for the message to be published to the Scan topic
    moveID  ID number for the message to be published to the MovementCommand topic
    '''
    def run(self, cr, scanID, moveID):
        self.nextState = "MoveDigState"
        if self.movedSoFar >= self.digSiteDist:
            self.binCheck(scanID)

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
        return (scanID+1, moveID)

    #keep instance of MoveDigState to update next move
    def setMoveDig(self, digState):
        self.moveDigState = digState    

    #check if the robot is in the excavation zone
    def binCheck(self, id):        
        #begin scanning lidar
        crossSection, distance = rasp.scan(self.pub, False, id) 
        #if in excavation site set the next state to DigState
