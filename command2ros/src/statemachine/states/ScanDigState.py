from states.State import State
<<<<<<< HEAD
from states.State import MoveDigState
from MovementData import MovementData
=======
from LidarCommands import raspi_threads as rasp
from LidarCommands.constants import *
>>>>>>> c06ff52c9b406d9f208cceb659fa1edea3359ece

class ScanDigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ScanDigState", "MoveDigState")
        self.MoveDigState = None

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")

        #thoughts: three threads- produce, consume, send data from LiDAR
        #use modified old code, for basics of plan see comments directly below

        #scan with LiDAR

        #A: create map for laptop
        #A: send map to laptop
        #A: receive move instructions from laptop

        #B: create map for AI
        #B: interpret map for AI & get move instructions

    def setMoveDig(self, digState):
        self.MoveDigState = digState
