from states.State import State
from LidarCommands import raspi_threads as rasp
from LidarCommands.constants import *

class ScanDumpState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ScanDumpState", "MoveDumpState")

    #implementation for each state: overridden
    def run(self):
        print("\n>run() not implemented\n")        
