#!/usr/bin/env python3

import time
import sys
sys.path.append("/home/pi/ros_catkin_ws/src/command2ros/src/statemachine/")

import rospy
import roslib
roslib.load_manifest('command2ros')

from command2ros.msg import MovementCommand
from command2ros.msg import ScanCommand
from command2ros.msg import ArduinoMessage
from CommandRobot import CommandRobot
from FeedbackHandler import FeedbackHandler

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
        end = False
        scanID = 0
        moveID = 0
        print("robot is starting")
        movementPub, scanPub = self.rosSetup()  
        print("ros has been set up")  
        feedbackHandler = FeedbackHandler()
        feedbackHandler.start()
        print("feedback handler set up")       
        dd = self.dataDistributorSetup(movementPub) 
        print("data distributor to send commands is set up") 

        #use to update the next command and send to arduino mega
        cr = CommandRobot()
        print("command robot is ready to command")

        print("Starting in manual command mode")

        while(True):
            scanID, moveID = self.currentState.run(cr, scanPub, scanID, moveID, feedbackHandler.progressMessage)            
            
            if self.currentState.autonomousMode:
                print("switching from manual mode to autonomous mode")
                self.currentState = self.StartState 
                break  
            elif self.currentState.endProgram:
                end = True
                print("ending the program")
                break

        while not end:
            print("run the next state")
            self.currentState.run(cr)    

            print("send command")
            cr.sendCommand()       

            #set the current state to the specified next state
            next = self.currentState.nextState
            self.setNext(next) 

        if end:         
            print("command robot stopped")    
            dd.join()            
            print("data distributor stopped")
            time.sleep(2)
            exit()
        return

    #set next state
    def setNext(self, next):
        if next == self.MoveDigState.name:
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
        return dataDist

    #ros node for program and publisher for movement commands
    def rosSetup(self):
        #create ros publisher to update/send data
        movementPub = rospy.Publisher('MovementCommand', MovementCommand, queue_size=10)
        scanPub = rospy.Publisher('Scan', ScanCommand, queue_size=10)
        rospy.init_node('command2ros', anonymous=True)
        return (movementPub, scanPub)

#PROGRAM ENTRY
if __name__ == "__main__":
    sm = StateMachine()
    sm.startRobot()
