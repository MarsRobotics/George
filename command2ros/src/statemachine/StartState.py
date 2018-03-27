from states.State import State

class StartState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("Start", "ScanDig")
        self.transitionReady = False

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")

        #always begin with no transition
        self.transitionReady = False
        
        #move wheels to starting position
        #if wheels are in correct position
        self.transitionReady = True

    #implementation for each state: overridden
    def transition(self):
        return self.transitionReady