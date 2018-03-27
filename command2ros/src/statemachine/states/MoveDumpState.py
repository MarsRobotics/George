from states.State import State
from states.ScanDumpState import ScanDumpState

class MoveDumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("MoveDumpState", "ScanDumpState")

    #implementation for each state: overridden
    def run(self, moveInstructions):
        print("\n>run() not implemented\n")
