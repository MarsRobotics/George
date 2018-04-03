#!/usr/bin/env python3

import rospy
from command2ros.msg import ArduinoMessage
from FeedbackData import FeedbackData
import threading

class FeedbackHandler(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.messageQueue = []
        return    

    def run(self):
        self.listener()

    def callback(self, data):
        feedback = FeedbackData()
        feedback.ready = data.ready
        feedback.messageID = data.messageID
        feedback.serialID = data.serialID
        feedback.progress = data.progress
        feedback.errorDriving = data.errorDriving
        feedback.errorDigging = data.errorDigging
        feedback.errorDumping = data.errorDumping
        feedback.errorTurning = data.errorTurning
        self.messageQueue.append(feedback)        

    def listener(self):        
        rospy.Subscriber("ArduinoFeedback", ArduinoMessage, self.callback)
        rospy.spin()