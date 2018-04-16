from states.State import State
from MovementData import MovementData

class DigState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("DigState", "ScanDumpState")
        
    '''
    Run for DigState:   Excavate

    cr      CommandRobot allows commands to be published to the Mega
    scanID  ID number for the message to be published to the Scan topic
    moveID  ID number for the message to be published to the MovementCommand topic
    '''
    def run(self, cr, scanID, moveID):
        print("Command robot to excavate")
        dig_data = MovementData()
        dig_data.dig = True
        dig_data.serialID = moveID  
        cr.setCommand(dig_data)
        print("send command")
        cr.sendCommand()    
        return (scanID, moveID+1)