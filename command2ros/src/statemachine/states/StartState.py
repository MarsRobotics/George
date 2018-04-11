from states.State import State
from MovementData import MovementData

class StartState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("StartState", "ScanDigState")

    #implementation for each state: overridden
    def run(self, cr, id):
        print("\n>run() not implemented\n")
