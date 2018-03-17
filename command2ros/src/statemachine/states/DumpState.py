from states.State import State

class DumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("Dump", "ScanDig")
        self.transitionReady = False

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")