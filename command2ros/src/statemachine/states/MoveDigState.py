from states.State import State
from states.ScanDigState import ScanDigState
from MovementData import MovementData

class MoveDigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("MoveDigState", "ScanDigState")
        self.moveCommand = MovementData()

    #implementation for each state: overridden
    def run(self, cr, id):
        self.moveCommand.serialID = id
        cr.setCommand(self.moveCommand)
        print("send command")
        cr.sendCommand()    

    def setNextMove(self, newMove):        
        self.moveCommand = newMove
