#!/usr/bin/env python3
"""
MovementData        Define movement for robot      
"""
class MovementData:
    
    def __init__(self):
        self.driveDist = 0      #distance to drive forward in meters
        self.turn = 0           #degrees to turn robot
        self.dig = False
        self.dump = False
        self.packin = False     #ending sequence, wheels roll in so tucked under
        self.eStop = False      
        self.pause = False

        self.serialID = 0
        self.cancel = False
        self.manualDrive = 0
        self.manualTurn = 0
        self.manual = False

        self.endProgram = False #not part of MovementCommand.msg for publishing
        return
