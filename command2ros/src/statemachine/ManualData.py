#!/usr/bin/env python3
"""
ManualData        Define movement for robot      
"""
class ManualData:
    
    def __init__(self):
        self.drive = 0
        self.turn = 0
        self.dig = 0
        self.raiseForDig = 0
        self.dump = 0
        self.packin = False     #ending sequence, wheels roll in so tucked under
        self.forwardScan = False 
        self.backwardScan = False 
        self.manualDrive = 0
        self.manualTurn = 0
        self.stop = False
        self.autonomousMode = False
        self.endProgram = False
        self.cameraNum = 0
        return
