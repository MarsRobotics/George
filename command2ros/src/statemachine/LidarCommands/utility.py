
__author__="Sully Cothran, Jaimiey Sears"
__copyright__="October 26, 2015"
__version__= 1.0

import math, time, pickle
import datetime as dt
from LidarCommands.constants import *
# from openpyxl import Workbook
# from openpyxl.cell import get_column_letter as toLetter

def decode_new(string, anglePhi):
    splitData = splitNparts(string, 3)#Split into three letter strings
    resolution = 1#1 degree per scan
    #init the result lists
    dists = []
    x = []
    y = []
    z = []
    phis = []
    thetas = []

    # get starting angle from constants
    angleTheta = START_ANGLE

    # decode all 3-letter string values to numeric values
    for point in splitData:
        dists.append(decodeShort(point))

    # translate to XYZ-coords based on angleTheta and anglePhi
    for dist in dists:
        #find the cartesian coordinates
        xCoord = dist*math.cos(angleTheta)
        yCoord = dist*math.sin(angleTheta)

        zCoord = yCoord*(-1*math.sin(anglePhi))
        yCoord = yCoord*math.cos(anglePhi)
        

        x.append(xCoord)
        y.append(yCoord)
        z.append(zCoord)
        phis.append(anglePhi)
        thetas.append(angleTheta)

        angleTheta += resolution

    return x, y, z, dists, phis, thetas



# def decode(string, angle, scanStartAngle):
#     #get the first letter of the result string
#     firstLetter = string[0]
#     lastLetter = string[len(string)-1]
#
#     #set the resolution (for default, .25 degrees per scan)
#     resolution = 0.25
#
#     #output data
#     dataOutput = ""
#
#     #init the result lists
#     dists = []
#     x = []
#     y = []
#     z = []
#     phis = []
#     thetas = []
#
#     # #pre calculate sine of phi and cosine of phi
#     # sinePhi = math.sin(math.pi/2)
#     # cosPhi = math.cos(math.pi/2)
#
#     #set the number of chars per result based off of first letter of result string
#     NUM_CHARS = 3
#
#     #for each set of char values, decode the distance value and determine cartesian coords
#     count = 0
#     for i in range(NUM_CHARS - 1, len(string)-1, NUM_CHARS):
#
#         # record phi
#         phis.append(angle)
#
#         # Just decode an N-letter section of the data
#         dist = decodeShort(string[i-(NUM_CHARS-1):i+1])
#         dists.append(dist)
#
#         #get the current angle of the scanner for this value (may need to be changed for values)
#         currentAngle = math.radians(scanStartAngle + count*RESOLUTION)
#         thetas.append(currentAngle)
#
#         #find the cartesian coordinates
#         xCoord = dist*math.cos(currentAngle)
#         yCoord = dist*math.sin(currentAngle)
#         # zCoord = 0    # value*cosPhi
#
#         yc = yCoord*math.cos(angle)
#         zc = yCoord*(-1*math.sin(angle))
#
#         yCoord = yc
#         zCoord = zc
#
#         # print coords
#         xCoord = smallToZero(xCoord)
#         yCoord = smallToZero(yCoord)
#         zCoord = smallToZero(zCoord)
#
#         dataOutput += "Angle: " + str(math.degrees(currentAngle)) + " Dist: " + str(dist/10) +  " X: " + str(xCoord) + " Y: " + str(yCoord) + " Z: " + str(zCoord) + '\n'
#         #add values to results
#         x.append(xCoord)
#         y.append(yCoord)
#         z.append(zCoord)
#         count += 1
#
#     # print "Final Count: " + str(count)
#     # print "Distances: ", dists
#     return x, y, z, scanStartAngle + count*resolution, dataOutput, phis, thetas, dists

def splitNparts(string, n):
    doSplit = True
    strList = []
    while(doSplit):
        if string == "":
            return strList
        if(len(string) < n):
            strList.append(string)
            return strList
        else:
            strList.append(string[0:n])
            string = string[n:len(string)]


def smallToZero(val):
    if abs(val) < .001:
        return 0
    return val

def decodeShort(dataStr):
    result = 0
    for i in range(len(dataStr)):
        index = len(dataStr)-1-i
        #Get the lower value
        temp = (ord(dataStr[index]) - 0x30) << (i*6)

        #put the value together with rest
        result += temp

    return result

def generateStampedFileName(ext):
    timestamp = dt.datetime.now()
    return "test_vectors_{}_{}_{}_{}_{}_{}{}".format(timestamp.year, timestamp.month, timestamp.day,\
           timestamp.hour, timestamp.minute, timestamp.second, ext)

# Writes an object to a pickle file
def writeToPickle(filename, obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
        debugPrint("Pickle file {} written".format(filename), ROSTA)


# def pickle2xlsx(filename):
#     dataArrays = None
#     try:
#         with open(filename, 'rb') as f:
#             dataArrays = pickle.load(f)
#     except:
#         return OPERATION_FAILURE
#     wbSave(generateStampedFileName('.xlsx'), dataArrays)
#     debugPrint("Wrote .xlsx file", UTILITY)
#     return OPERATION_SUCCESS


##
# debugPrint
#
# Description: prints the specified string only when debug boolean is set to True
#
# __params__
##
def debugPrint(string, lvl):
    if lvl in DEBUG_LEVELS:
        print("{}\t\t{}".format("DEBUG LOG:",string))
    return

# Saves a workbook (MS Excel)
# def wbSave(filename, dataArrays):
#     # write to excel workbook
#     wb = Workbook()
#     # outfile = load_workbook(filename=generateStampedFileName(), read_only=False, keep_vba=True)
#     sheet1 = wb.active
#     # sheet1 = outfile.active
#     sheet1['A1'] = "X"
#     sheet1['B1'] = "Y"
#     sheet1['C1'] = "Z"
#     sheet1['D1'] = "Phi"
#     sheet1['E1'] = "Theta"
#     sheet1['F1'] = "Dist"
#     sheet1['G1'] = "Time"
#
#     # insert x y z into excel document
#     for i in range(len(dataArrays)):
#         dataset = dataArrays[i]
#         for j in range(len(dataset)):
#             cell = '{}{}'.format(toLetter(i+1),j+2)
#             sheet1[cell] = dataset[j]
#
#     wb.save(filename)
#     debugPrint("workbook saved as {}".format(filename), ROSTA)


## UNIT TESTS FOR DECODE ##
# debugPrint("Unit test 1", UTILITY)
# X, Y, Z, scanAngle, dataOutput, TH, PHI, DIST= decode(str('0CB0'), 0, 0)
# if dataOutput == str('Angle: 0.0 Dist: 123 X: 1234.0 Y: 0 Z: 0\n'): debugPrint( "Long Decode Passed.\n", UTILITY)
# else: debugPrint("Long decode failed with {}\n".format(dataOutput), UTILITY)

debugPrint( "Unit test 2", UTILITY)
result = decodeShort(str('CB'))
if str(result) == str('1234'): debugPrint("Short decode Passed.\n", UTILITY)
else: debugPrint( "Short decode failed with {}".format(result), UTILITY)

debugPrint( "Unit test 3", UTILITY)
result = splitNparts("HelloHelloHello",5)
if result == ["Hello", "Hello","Hello"]: debugPrint( "Split 5 Parts Passed.\n", UTILITY)
else: debugPrint( "Split 5 Failed with {}".format(result), UTILITY)

debugPrint( "Unit test 4", UTILITY)
result = splitNparts("HelloHelloHello",4)
if result == ["Hell", "oHel","loHe","llo"]: debugPrint("Split 4 Parts Passed.\n", UTILITY)
else: debugPrint( "Split 4 Failed with {}".format(result), UTILITY)

# pickle2xlsx("test_vectors_2015_12_10_19_20_21.dat")
