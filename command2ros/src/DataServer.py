#!/usr/bin/env python3
import sys
sys.path.append("/home/pi/ros_catkin_ws/src/command2ros/src/")
import rospy
import roslib
import time
import socket
import threading

from CommandRobot import CommandRobot
from MovementData import MovementData
from DataTransferProtocol import receiveData, sendData
from command2ros.msg import MovementCommand

roslib.load_manifest('command2ros')

sendRate = 10 #Hz #**sendRate = rospy.Rate(10) #Hz

"""
DataDistributor     Create threads to control network connections
                    from clients
"""
class DataDistributor(threading.Thread):

    def __init__(self):
        self.data = MovementData()
        threading.Thread.__init__(self)
        return

    #set up socket to receive incoming requests
    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("192.168.1.45", 10000)) #George, localhost to make faster?
        server.listen(1) #backlog is 1

        #accept connections and spawn thread to handle
        #until server closes
        while True:
            (clientSocket, address) = server.accept()
            cs = DataServer(clientSocket, self, address)
            cs.run()
        return

"""
DataServer      Manage connection to a given client, receives and
                sends commands
"""
class DataServer(threading.Thread):

    def __init__(self, socket, distributor, address):
        self.socket = socket
        self.distributor = distributor #George
        self.address = address         

        threading.Thread.__init__(self)
        return

    def run(self):
        try:
            sendTime = 0

            while True: #**not rospy.is_shutdown():
                self.socket.setblocking(1)

                #send last movement data to the client if time has passed
                if sendTime < time.time(): #**delete
                    sendData(self.socket, self.distributor.data)
                    sendTime = time.time() + 1/float(sendRate) #**sendRate.sleep()

                try:
                    self.socket.setblocking(0)

                    #get new command
                    newCommand = receiveData(self.socket)

                    #add command to execution queue
                    if newCommand.eStop:
                        commandQueue.insert(0, newCommand)
                    else:
                        commandQueue.append(newCommand)
                except socket.error:
                    continue
        except socket.error: 
            #lost connection, stop robot
            newCommand = MovementData()
            newCommand.eStop = True
            commandQueue.insert(0, newCommand)
            return
        return

#queue for sending movement commands to motors
commandQueue = []

#handles connections between clients
dataDist = DataDistributor()
dataDist.start()

#create ros publisher to update/send data
pub = rospy.Publisher('MovementCommand', queue_size=10)
rospy.init_node('command2ros', anonymous=True)

#start receiving movement commands
cr = CommandRobot()
cr.createConnection()

#publish commands to arduino
while True:
    if len(commandQueue) > 0:
        command = commandQueue.pop(0)

        #update to the next command
        mc = MovementCommand()
        mc.driveDist = command.driveDist #distance to drive meters  
        mc.turn = command.turn           #degrees for articulation motors
        mc.packin = command.packin       #ending sequence, wheels tucked under
        mc.eStop = command.eStop         #stop robot TODO:eStop and stop?
        pub.publish(mc)
