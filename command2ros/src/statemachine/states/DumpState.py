from states.State import State
from MovementData import MovementData

class DumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("DumpState", "ScanDigState")

    '''
    Run for DumpState:  Deposit the icy regolith in the collection bin

    cr      CommandRobot allows commands to be published to the Mega
    scanID  ID number for the message to be published to the Scan topic
    moveID  ID number for the message to be published to the MovementCommand topic
    '''
    def run(self, cr, scanID, moveID):
        dump_data = MovementData()
        dump_data.dump = True
        dump_data.serialID = moveID
        cr.setCommand(dump_data)        
        print("send command")
        cr.sendCommand()       
        return (scanID, moveID+1)
