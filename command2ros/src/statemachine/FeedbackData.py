#!/usr/bin/env python3

class FeedbackData:

    def __init__(self):
        self.ready = False
        self.messageID = 0
        self.serialID = 0
        self.progress = ""
        self.errorDriving = False
        self.errorDigging = False
        self.errorDumping = False
        self.errorTurning = False
        self.digVal = 0
        return