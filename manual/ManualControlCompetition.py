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
 space           stop everything, cancelling current execution
 r               raise digger
 l               lower digger
 c               collect gravel
 u               unwind digger (run in reverse)
 p               pack in
 d               dump
 s               drive forward slow
 0               lower & dig
 1               dig & drive forward slowly
 2               dig & drive forward slowly & lower
 3               lower & drive normal
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
    elif key == KeyCode.from_char('s'):
        data.manualDrive = 2
        print("Set command to drive slowly")
        sendData(sock, data)
    elif key == KeyCode.from_char('0'):
        data.raiseForDig = -1
        speed = int(input("Speed: "))
        data.dig = speed
        print("Set command to lower and dig")
        sendData(sock, data)
    elif key == KeyCode.from_char('1'):
        data.manualDrive = 2
        speed = int(input("Speed: "))
        data.dig = speed
        print("Set command to lower and dig")
        sendData(sock, data)
    elif key == KeyCode.from_char('2'):
        data.raiseForDig = -1
        speed = int(input("Speed: "))
        data.dig = speed
        data.manualDrive = 2
        print("Set command to lower, dig, drive forward slowly")
        sendData(sock, data)
    elif key == KeyCode.from_char('3'):
        data.raiseForDig = -1
        data.manualDrive = 1
        print("Set command to lower and drive normal")
        sendData(sock, data)
    elif key == Key.down:  
        data.manualDrive = -1
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
    elif key == KeyCode.from_char('r'):
        data.raiseForDig = 1
        print("Set command to raise digger")
        sendData(sock, data)
    elif key == KeyCode.from_char('l'):
        data.raiseForDig = -1
        print("Set command to lower digger")
        sendData(sock, data)
    elif key == KeyCode.from_char('c'):
        speed = int(input("Speed: "))
        data.dig = speed
        print("Set command to dig (collect)")
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