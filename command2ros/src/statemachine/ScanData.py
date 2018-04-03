#!/usr/bin/env python3
"""
ScanData        Define scan data for LiDAR
"""

class ScanData:

    def __init__(self):
        self.serialID = 0
        self.scanForward = True #scan backwards if false