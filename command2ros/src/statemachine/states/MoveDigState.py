from states.State import State
from states.ScanDigState import ScanDigState
from MovementData import MovementData

class MoveDigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("MoveDigState", "ScanDigState")
        self.moveCommand = MovementData()

    '''
    Run for MoveDigState:  Send movement command set by the ScanDigState
            to the Mega with updated ID

    cr      CommandRobot allows commands to be published to the Mega
    scanID  ID number for the message to be published to the Scan topic
    moveID  ID number for the message to be published to the MovementCommand topic
    '''
    def run(self, cr, scanID, moveID):
        self.moveCommand.serialID = moveID
        cr.setCommand(self.moveCommand)
        print("send command")
        cr.sendCommand()   
        return (scanID, moveID)

    #set the next move for the robot
    def setNextMove(self, newMove):        
        self.moveCommand = newMove
