from states.State import State
from MovementData import MovementData

class DumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("DumpState", "ScanDigState")
        self.transitionReady = False

    #implementation for each state: overridden
    def run(self, cr, id):
        #new movement data with command dump set to true
        dump_data = MovementData()
        dump_data.dump = True
        dump_data.serialID = id
        id += 1
        cr.setCommand(dump_data)        
        print("send command")
        cr.sendCommand()       
        return id
