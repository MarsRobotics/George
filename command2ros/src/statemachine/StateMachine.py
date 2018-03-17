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

        #set current state
        self.currentState = self.StartState

        #transition criteria
        self.inExcavationZone = False
        self.hopperEmpty = True
        self.inDumpZone = False

    #control program
    def startRobot(self):
        pub = self.rosSetup()
        self.dataDistributorSetup(pub)
        #start receiving movement commands
        cr = CommandRobot()
        cr.createConnection()

        print("\n>main() not implemented\n")

    def dataDistributorSetup(self, pub):
        #handles connection to client to receive commands
        dataDist = DataDistributor(pub)
        dataDist.start()

    def rosSetup(self):
        #create ros publisher to update/send data
        pub = rospy.Publisher('MovementCommand', MovementCommand, queue_size=10)
        rospy.init_node('command2ros', anonymous=True)
        return pub

#PROGRAM ENTRY
if __name__ == "__main__":
    sm = StateMachine()
    sm.startRobot()