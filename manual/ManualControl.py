from ManualData import ManualData
from pynput.keyboard import Key, Listener, KeyCode
import socket 
import sys
from DataTransferProtocol import sendData, receiveData
import time

'''
Key press       Command
 up              drive forward
 down            drive backwards
 right           turn right
 left            turn left
 space           stop
 e               excavate
 p               pack in
 d               dump
 a               autonomous mode
 f               scan forward
 b               scan backwards
 1               drive 100 forwards
 2               drive 100 backwards
'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",20000))
print("binding")
s.listen(1)
print("listening")
(sock,address) = s.accept()
print("accepted connection")

def on_press(key):
    data = ManualData()
    if key == Key.up:
        data.manualDrive = 1
        print("Set command to drive forward")
        sendData(sock, data)
    elif key == Key.down:  
        data.manualDrive = -1
        print("Set command to drive backwards")
        sendData(sock, data)
    elif key == KeyCode.from_char('1'):  
        data.drive = 100
        print("Set command to drive backwards")
        sendData(sock, data)
    elif key == KeyCode.from_char('2'):  
        data.drive = -100
        print("Set command to drive backwards")
        sendData(sock, data)
    elif key == Key.right:
        data.manualTurn = 1
        print("Set command to turn right")
        sendData(sock, data)
    elif key == Key.left:
        data.manualTurn = -1   
        print("Set command to turn left")
        sendData(sock, data)
    elif key == KeyCode.from_char('e'):
        data.dig = True
        print("Set command to excavate")
        sendData(sock, data)
    elif key == KeyCode.from_char('p'):
        data.packin = True
        print("Set command to pack in")
        sendData(sock, data)
    elif key == KeyCode.from_char('d'):
        data.dump = True
        print("Set command to dump")
        sendData(sock, data)
    elif key == Key.space:
        data.stop = True
        print("Set command to stop")
        sendData(sock, data)
    elif key == KeyCode.from_char('f'):
        data.forwardScan = True
        print("Scan LiDAR forward")
        sendData(sock, data)
    elif key == KeyCode.from_char('b') :
        data.backwardScan = True
        print("Scan LiDAR backwards")
        sendData(sock, data)
    elif key == KeyCode.from_char('a'):
        data.autonomousMode = True
        print("switch from manual to autonomous")
        sendData(sock, data)
    else:
        print("Not a valid command")

def on_release(key):
    if key == Key.esc:
        data = ManualData()
        data.endProgram = True
        sendData(sock, data)
        time.sleep(2)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return False

with Listener(on_press=on_press, on_release=on_release) as l:
    l.join()
        