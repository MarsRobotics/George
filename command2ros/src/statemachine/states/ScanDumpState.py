from states.State import State
from MovementData import MovementData

class ScanDumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ScanDumpState", "MoveDumpState")
        self.MoveDumpState = None

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")        

    def setMoveDump(self, moveDumpState):
        self.MoveDumpState = moveDumpState
