from states.State import State
from states.ScanDumpState import ScanDumpState
from MovementData import MovementData

class MoveDumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("MoveDumpState", "ScanDumpState")
        self.moveCommand = MovementData()

    #implementation for each state: overridden
    def run(self, cr, id):
        self.moveCommand.serialID = id
        cr.setCommand(self.moveCommand)
        print("send command")
        cr.sendCommand()

    #set the next move for the robot
    def setNextMove(self, newMove):
        self.moveCommand = newMove
