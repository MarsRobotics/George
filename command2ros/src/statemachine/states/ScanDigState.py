from states.State import State

class ScanDigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ScanDigState", "MoveDigState")

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")

        #thoughts: three threads- produce, consume, send data from LiDAR
        #use modified old code, for basics of plan see comments directly below

        #scan with LiDAR

        #A: create map for laptop
        #A: send map to laptop
        #A: receive move instructions from laptop

        #B: create map for AI
        #B: interpret map for AI & get move instructions
