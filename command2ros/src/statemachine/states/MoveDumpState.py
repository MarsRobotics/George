from states.State import State
from MovementData import MovementData

class MoveDumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("MoveDumpState", "ScanDumpState")
        self.moveCommand = MovementData()

    '''
    Run for MoveDumpState:  Send movement command set by the ScanDumpState
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
        return (scanID, moveID+1)

    #set the next move for the robot
    def setNextMove(self, newMove):
        self.moveCommand = newMove
