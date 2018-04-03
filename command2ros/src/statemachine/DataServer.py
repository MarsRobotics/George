#!/usr/bin/env python3
import sys
import rospy
import roslib
import time
import socket
import threading

#from CommandRobot import CommandRobot
from MovementData import MovementData
from DataTransferProtocol import receiveData, sendData
from command2ros.msg import MovementCommand

"""
DataDistributor     Receive new commands and create service to 
                    maintain queue of commands and publish when 
                    the arduino is ready to receive commands
"""
class DataDistributor(threading.Thread):

    def __init__(self, pub):
        self.data = MovementData()      
        self.pub = pub  
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()        
        return

    #create connection to receive commands
    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 10000)) #George
        server.listen(5)                  #accept only one connection        

        #begin publisher mechanism
        dataServer = DataServer(self.pub)
        dataServer.start()

        #create connection to receive commands
        (clientSocket, address) = server.accept()        

        #begin receiving commands
        self.getCommands(dataServer, clientSocket, server)              
        return

    #prepare thread to finish execution
    def stop(self):
        self._stop_event.set()
    
    #receive new movement commands 
    def getCommands(self, dataServer, clientSocket, server):
        print("Running")
        sendRate = rospy.Rate(10) #10 Hz
        try:
            while not rospy.is_shutdown():  
                try:
                    clientSocket.setblocking(1)

                    #get new command
                    newCommand = receiveData(clientSocket)

                    if newCommand.endProgram:
                        dataServer.stop()                        
                        dataServer.join()
                        print("data server is closed")                        
                        clientSocket.close()
                        print("datadistributor: clientsocket closed")
                        server.shutdown(socket.SHUT_RDWR)
                        server.close()
                        print("datadistributor: server closed") 
                        return
                    else:
                        #add command to execution queue
                        dataServer.addCommand(newCommand)                   
                except socket.error:
                    continue                                                
        except socket.error: 
            #lost connection, stop robot
            newCommand = MovementData()
            newCommand.eStop = True
            dataServer.addCommand(newCommand)
            return                       
        return

"""
DataServer      Stores all commands in a queue, publishes when Arduino is ready
                unless the next command is to eStop
"""
class DataServer(threading.Thread):

    def __init__(self, pub):
        self.pub = pub
        self.commandQueue = []               
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        return

    #prepare thread to finish execution
    def stop(self):
        self._stop_event.set()

    #add command to queue to be published
    def addCommand(self, newCommand):
        print("Inserting command")
        if newCommand.eStop:
            self.commandQueue.insert(0, newCommand)
        else:
            self.commandQueue.append(newCommand)
        return

    #publish next command
    def run(self):
        while True:
            #let thread terminate
            if self._stop_event.is_set():
                print("dataserver is closed")
                return

            #publish as long as there is a command to publish
            if len(self.commandQueue) > 0:
                command = self.commandQueue.pop(0)

                #update to the next command
                self.pub.publish(
			serialID=command.serialID,
			manual=command.manual,
			manualDrive=command.manualDrive,
			manualTurn=command.manualTurn,
			driveDist=command.driveDist, 
			turn=command.turn, 
			dig=command.dig, 
			dump=command.dump, 
			packin=command.packin, 
			eStop=command.eStop, 
			pause=command.pause,
			cancel=command.cancel)   
    
