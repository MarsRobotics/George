#!/usr/bin/env python3
"""
ManualData        Define movement for robot      
"""
class ManualData:
    
    def __init__(self):
        self.dig = False
        self.dump = False
        self.packin = False     #ending sequence, wheels roll in so tucked under
        self.forwardScan = False 
        self.backwardScan = False 
        self.manualDrive = 0
        self.manualTurn = 0
        self.stop = False
        self.autonomousMode = False
        self.endProgram = False
        self.drive = 0
        self.turn = 0
        return

