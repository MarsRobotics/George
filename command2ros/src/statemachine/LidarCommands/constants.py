__author__ = 'Jaimiey Sears and Alex Schendel'

####### GENERAL PURPOSE CONSTANTS #######
OPERATION_SUCCESS = 0
OPERATION_FAILURE = -1

# indexes of lidar data in processedDataArrays
X_IDX = 0
Y_IDX = 1
Z_IDX = 2
D_IDX = 3
PHI_IDX = 4
TH_IDX = 5


# Starting theta angle of our scans
START_ANGLE = 0

# Resolution of LIDAR scans. this should change based on grouping
RESOLUTION = 0.25

####### DEBUG MESSAGE CONSTANTS #######
# Debug level for different message levels.
# 0 = only essential messages
# 1 = print ROSta messages
# 2 = print producer and consumer messages
# 3 = print producer and consumer data
# 4 = print data as it is processed (for use in utility.py)
ROSTA = 1
SOCKET_MSG = 2
SOCKET_DATA = 3
UTILITY = 4
SERVO_DRIVER = 5
DEBUG_LEVELS = [ROSTA, SERVO_DRIVER, SOCKET_MSG, SOCKET_DATA]


####### SERVO CONTROL CONSTANTS #######
#initial setup
# pwm frequency is 50 Hz
#PWM_FREQ = 50

# connect to BCM pin 21 on RPi
SERVO_PIN = 21
# pwm range is 1.8 to 11.9... 5 to 10? (1 ms to 2 ms)
#Update: Website says 553 to 2520 us (2.765 to 12.6)
# FOR HS-645MG
#PWM_MIN = 2.765
#PWM_MAX = 12.6
#DEGREE_MIN = 0
#DEGREE_MAX = 197 #Website also says it can rotate up to 197 degrees

#For TowerPro SG-5010
#1 ms to 2 ms (5 to 10)
#Note: 1 ms is -90 degrees to 2 ms is +90 degrees, so defining this from 0 to 180 will just change the origin
#PWM_MIN = 5.0
#PWM_MAX = 10.0
#DEGREE_MIN = 0
#DEGREE_MAX = 180