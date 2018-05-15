from ManualData import ManualData
from pynput.keyboard import Key, Listener, KeyCode
import socket 
import sys
from DataTransferProtocol import sendData, receiveData
import time
import cv2

'''
Key press       Command
 up              drive forward
 2               drive forward slowly
 down            drive backwards
 right           turn right
 left            turn left
 space           stop everything, cancelling current execution
 r               raise digger
 l               lower digger
 c               collect gravel
 u               unwind digger (run in reverse) 0 - 120
 p               pack in
 d               dump -100 - 100
 s               send data except for: left, right, stop, packin
'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",20000))
print("binding")
s.listen(1)
print("listening")
sock, address = s.accept()
print("accepted connection")

def press(key, start):  
    change = True
    if start == "":
        data = ManualData()
    else:
        data = start

    if key == Key.up:
        data.manualDrive = 1
        print("Set command to drive forward")        
    elif key == KeyCode.from_char('2'):        
        data.manualDrive = 2
        print("Set command to drive forward slowly")
    elif key == Key.down:  
        data.manualDrive = -1
        print("Set command to drive backwards")
    elif key == Key.right:
        data.manualTurn = 1
        sendData(sock, data)
        print("Send command to turn right ***")
    elif key == Key.left:
        data.manualTurn = -1 
        sendData(sock, data)
        print("Send command to turn left ***")
    elif key == KeyCode.from_char('r'):
        data.raiseForDig = 1
        print("Set command to raise digger")
    elif key == KeyCode.from_char('l'):
        data.raiseForDig = -1
        print("Set command to lower digger")
    elif key == KeyCode.from_char('c'):
        speed = int(input("Dig speed: "))
        data.dig = speed
        print("Set command to dig (collect)")
    elif key == KeyCode.from_char('p'):
        data.packin = True
        sendData(sock, data)
        print("Send command to pack in ***")
    elif key == KeyCode.from_char('d'):
        speed = int(input("Dump speed: "))
        data.dump = speed
        print("Set command to dump")
    elif key == Key.space:        
        data.stop = True
        sendData(sock, data)
        print("Send command to stop ***")
    elif key == KeyCode.from_char('s'):        
        print("-----Send command-----")
        sendData(sock, data)
    else:
        change = False
        print("Not a valid command")

    if change:
        return data
    else:
        return ""
    
def on_release(key):
    if key == Key.esc:
        d = ManualData()
        d.endProgram = True
        sendData(sock, d)
        time.sleep(2)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return False

def on_press(key):
    if key == KeyCode.from_char('n'):
        press(key, True)
    elif key == KeyCode.from_char('')

with Listener(on_press=on_press, on_release=on_release as l:
    l.join()