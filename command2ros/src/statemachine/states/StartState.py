from states.State import State

class StartState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("StartState", "ScanDigState")

    #implementation for each state: overridden
    def run(self,cr):
        print("\n>run() not implemented\n")
