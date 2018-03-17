from states.State import State

class DigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("Dig", "ScanDump")

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")