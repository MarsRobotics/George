import cv2

cam=0#TODO get cam int from socket

def videoSteam():
    frontCam = cv2.VideoCapture(0)#camera for maneuvering the field
    digCam = cv2.VideoCapture(1)#camera to tell how digging is working
    backCam = cv2.VideoCapture(2)#camera for backing up and docking to hopper
    while True:
        ret = None
        frame = None
        if cam == 2:
            ret, frame = backCam.read()#capture a frame from the back cam
        elif cam == 1:
            ret, frame = digCam.read()
        else:            
            ret, frame = frontCam.read()#default is the front 
        cv2.imshow('frame', frame)#TODO send frame over socket and display on laptop instead        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break#remove this if statement when displaying on laptop
    cv2.release()
    cv2.destroyAllWindows()

videoSteam()