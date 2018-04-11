from states.State import State
from MovementData import MovementData

class DigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("DigState", "ScanDumpState")
        

    #implementation for each state: overridden
    def run(self, cr):
        #new movement data with command dig set to true
        dig_data = MovementData()
        dig_data.dig = True
        cr.setCommand(dig_data)
