from states.State import State
from states.ScanDigState import ScanDigState
from MovementData import MovementData

class MoveDigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("MoveDigState", "ScanDigState")
        self.nextMove = MovementData()

    #implementation for each state: overridden
    def run(self, moveInstructions):
        print("\n>run() not implemented\n")

    def setNextMove(self, newMove):
        self.nextMove = newMove
