from states.State import State

class DumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("Dump", "ScanDig")
        self.transitionReady = False

    #implementation for each state: overridden
    def run(self, cr):
        #new movement data with command dump set to true
        dump_data = MovementData()
        dump_data.dump = True
        cr.setCommand(dump_data)
