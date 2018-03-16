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
        server.bind(("127.0.0.1", 10000)) #George
        server.listen(1) #backlog is 1

        #create connection
        (clientSocket, address) = server.accept()
        dataServer = DataServer()
        print("Running connection")
        dataServer.start()
        self.getCommands(dataServer, clientSocket, server)              
        return
    
    def getCommands(self, dataServer, clientSocket, server):
        print("Running")
        try:
            sendTime = 0

            while True: #**not rospy.is_shutdown():
                clientSocket.setblocking(1)

                #send last movement data to the client if time has passed
                if sendTime < time.time(): #**delete
                    sendData(clientSocket, self.data)
                    sendTime = time.time() + 1/float(sendRate) #**sendRate.sleep()

                try:
                    clientSocket.setblocking(0)

                    #get new command
                    newCommand = receiveData(clientSocket)

                    #add command to execution queue
                    print(newCommand.driveDist) 
                    dataServer.addCommand(newCommand)                   
                except socket.error:
                    continue                
                
                #e exits program, any other character continues 
                if sys.stdin.read(1).lower() == 'e':
                    clientSocket.shutdown(socket.SHUT_RDWR)
                    clientSocket.close()
                    server.shutdown(socket.SHUT_RDWR)
                    server.close()
                    dataServer.stop()
                    exit()
        except socket.error: 
            #lost connection, stop robot
            newCommand = MovementData()
            newCommand.eStop = True
            dataServer.addCommand(newCommand)
            return
        return

"""
DataServer      Manage connection to a given client, receives and
                sends commands
"""
class DataServer(threading.Thread):

    def __init__(self):
        self.commandQueue = []   #queue for sending movement commands to motors
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        return

    def stop(self):
        self._stop_event.set()

    def addCommand(self, newCommand):
        print("Inserting command")
        if newCommand.eStop:
            self.commandQueue.insert(0, newCommand)
        else:
            self.commandQueue.append(newCommand)
        return

    def run(self):
        while True:
            if self._stop_event.is_set():
                return

            if len(self.commandQueue) > 0:
                print("Command popped")    
                command = self.commandQueue.pop(0)
                print(command.driveDist)

                #update to the next command
                '''mc = MovementCommand()
                mc.driveDist = command.driveDist #distance to drive meters  
                mc.turn = command.turn           #degrees for articulation motors
                mc.dig = command.dig             
                mc.dump = command.dump    
                mc.packin = command.packin       #ending sequence, wheels tucked under
                mc.eStop = command.eStop         #stop robot TODO:eStop and stop?
                print(mc.driveDist)'''
                pub.publish(driveDist=command.driveDist, turn=command.turn, dig=command.dig, dump=command.dump, packin=command.packin, eStop=command.eStop, stop=command.stop)   

#handles connections between clients
dataDist = DataDistributor()
dataDist.start()

#create ros publisher to update/send data
pub = rospy.Publisher('MovementCommand', MovementCommand, queue_size=10)
rospy.init_node('command2ros', anonymous=True)

#start receiving movement commands
cr = CommandRobot()
cr.createConnection()
    
