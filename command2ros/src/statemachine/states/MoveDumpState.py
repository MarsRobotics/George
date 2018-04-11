from states.State import State
from states.ScanDumpState import ScanDumpState
from MovementData import MovementData

class MoveDumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("MoveDumpState", "ScanDumpState")
        self.nextMove = MovementData()

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")

    #set the next move for the robot
    def setNextMove(self, newMove):
        self.nextMove = newMove
