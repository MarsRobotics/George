from states.State import State
from states.ScanDigState import ScanDigState

class MoveDigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("MoveDigState", "ScanDigState")

    #implementation for each state: overridden
    def run(self, moveInstructions):
        print("\n>run() not implemented\n")
