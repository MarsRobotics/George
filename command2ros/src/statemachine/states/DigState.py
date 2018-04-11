from states.State import State
from MovementData import MovementData

class DigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("DigState", "ScanDumpState")
        

    #implementation for each state: overridden
    def run(self, cr, id):
        #new movement data with command dig set to true
        dig_data = MovementData()
        dig_data.dig = True
        dig_data.serialID = id   
        id += 1     
        cr.setCommand(dig_data)
        print("send command")
        cr.sendCommand()    
        return id