#!/usr/bin/env python3

import sys
sys.path.append("/home/pi/ros_catkin_ws/src/command2ros/src/statemachine/")

import rospy
import roslib
roslib.load_manifest('command2ros')

from command2ros.msg import MovementCommand
from CommandRobot import CommandRobot

from states.StartState import StartState
from states.ScanDigState import ScanDigState
from states.ScanDumpState import ScanDumpState
from states.MoveState import MoveState
from states.ManualMoveState import ManualMoveState
from states.DockingBinState import DockingBinState
from states.DigState import DigState
from states.DumpState import DumpState

from DataServer import DataDistributor

#track current state and program
class StateMachine():

    #init robot
    def __init__(self): 
        #init all states       
        self.StartState = StartState()
        self.ScanDigState = ScanDigState()
        self.ScanDumpState = ScanDumpState()
        self.MoveState = MoveState()
        self.DockingBinState = DockingBinState()
        self.DumpState = DumpState()
        self.DigState = DigState()
        
        self.ManualMoveState = ManualMoveState()

        #set current state
        self.currentState = self.StartState

        #transition criteria
        self.inExcavationZone = False   #ScanDigState to DigState
        self.hopperEmpty = True         #MoveState to ScanDigState if true, otherwise ScanDumpState
        self.inDumpZone = False         #ScanDumpState to DockingBinState

    #control program
    def startRobot(self):
        pub = self.rosSetup()           
        self.dataDistributorSetup(pub)  

        #use to update the next command and send to arduino 
        cr = CommandRobot()
        #self.currentState.run(cr)
        cr.sendCommand()     
        #set the current state to the specified next state
        self.currentState =  currentState.nextState

    #create distributor and server for movement commands
    def dataDistributorSetup(self, pub):
        #handles connection to client to receive commands
        dataDist = DataDistributor(pub)
        dataDist.start()

    #ros node for program and publisher for movement commands
    def rosSetup(self):
        #create ros publisher to update/send data
        pub = rospy.Publisher('MovementCommand', MovementCommand, queue_size=10)
        rospy.init_node('command2ros', anonymous=True)
        return pub

#PROGRAM ENTRY
if __name__ == "__main__":
    sm = StateMachine()
    sm.startRobot()
