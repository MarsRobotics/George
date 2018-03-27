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
from states.MoveDigState import MoveDigState
from states.MoveDumpState import MoveDumpState
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
        self.MoveDigState = MoveDigState()     
        self.MoveDumpState = MoveDumpState()   
        self.ScanDigState = ScanDigState()
        self.StartState = StartState()
        self.ScanDumpState = ScanDumpState()        
        self.DockingBinState = DockingBinState()
        self.DumpState = DumpState()
        self.DigState = DigState()
        
        self.ManualMoveState = ManualMoveState()

        #set current state
        self.currentState = self.ManualMoveState #self.StartState

        #transition criteria
        self.inExcavationZone = False   #ScanDigState to DigState
        self.hopperEmpty = True         #MoveState to ScanDigState if true, otherwise ScanDumpState
        self.inDumpZone = False         #ScanDumpState to DockingBinState        

    #control program
    def startRobot(self):
        print("robot is starting")
        pub = self.rosSetup()  
        print("ros has been set up")         
        self.dataDistributorSetup(pub) 
        print("data distributor to send commands is set up") 

        #use to update the next command and send to arduino 
        cr = CommandRobot()
        print("command robot is ready to command")

        while True:
            print("run the next state")
            self.currentState.run(cr)
            print("send command")
            cr.sendCommand()     
            #set the current state to the specified next state
            next = self.currentState.nextState
            self.setNext(next)

    #set next state
    def setNext(self, next):
        if next == self.ManualMoveState.name:
            self.currentState = self.ManualMoveState
        elif next == self.MoveDigState.name:
            self.currentState = self.MoveDigState
        elif next == self.MoveDumpState.name:
            self.currentState = self.MoveDumpState
        elif next == self.ScanDigState.name:
            self.currentState = self.ScanDigState
        elif next == self.ScanDumpState.name:
            self.currentState = self.ScanDumpState
        elif next == self.DockingBinState.name:
            self.currentState = self.DockingBinState
        elif next == self.DumpState.name:
            self.currentState = self.DumpState
        elif next == self.DigState.name:
            self.currentState = self.DigState

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
