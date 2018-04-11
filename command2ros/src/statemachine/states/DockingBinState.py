from states.State import State
from MovementData import MovementData

class DockingBinState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("DockingBinState", "DumpState")

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")
