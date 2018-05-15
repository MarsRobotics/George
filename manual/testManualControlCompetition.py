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

class ManualC():

    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",20000))
        print("binding")
        s.listen(1)
        print("listening")
        self.sock, address = s.accept()
        print("accepted connection")
        self.data = ManualData()

    def press(key):   
        if key == Key.up:
            self.data.manualDrive = 1
            print("Set command to drive forward")        
        elif key == KeyCode.from_char('2'):        
            self.data.manualDrive = 2
            print("Set command to drive forward slowly")
        elif key == Key.down:  
            self.data.manualDrive = -1
            print("Set command to drive backwards")
        elif key == Key.right:
            self.data.manualTurn = 1
            sendData(sock, self.data)
            self.data = ManualData()
            print("Send command to turn right ***")
        elif key == Key.left:
            self.data.manualTurn = -1 
            sendData(sock, self.data)
            self.data = ManualData()
            print("Send command to turn left ***")
        elif key == KeyCode.from_char('r'):
            self.data.raiseForDig = 1
            print("Set command to raise digger")
        elif key == KeyCode.from_char('l'):
            self.data.raiseForDig = -1
            print("Set command to lower digger")
        elif key == KeyCode.from_char('c'):
            speed = int(input("Dig speed: "))
            self.data.dig = speed
            print("Set command to dig (collect)")
        elif key == KeyCode.from_char('p'):
            self.data.packin = True
            sendData(sock, self.data)
            self.data = ManualData()
            print("Send command to pack in ***")
        elif key == KeyCode.from_char('d'):
            speed = int(input("Dump speed: "))
            self.data.dump = speed
            print("Set command to dump")
        elif key == Key.space:        
            self.data.stop = True
            sendData(sock, self.data)
            self.data = ManualData()
            print("Send command to stop ***")
        elif key == KeyCode.from_char('s'):        
            print("-----Send command-----")
            sendData(sock, self.data)
            self.data = ManualData()
        else:
            print("Not a valid command")
        
    def release(key):
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

m = ManualC()

with Listener(on_press=on_press, on_release=on_release) as l:
    l.join()

def on_press(key):   
    m.press(key)
    
def on_release(key):
    m.release(key)