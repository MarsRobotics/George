from states.State import State

class DigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("Dig", "ScanDump")
        

    #implementation for each state: overridden
    def run(self, cr):
        #new movement data with command dig set to true
        dig_data = MovementData()
        dig_data.dig = True
        cr.setCommand(dig_data)
