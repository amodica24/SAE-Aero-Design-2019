import random
import os
from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.models.status import TransmitStatus
import tkinter as tk
from tkinter import *
from tkinter import font
import sys
import datetime
import time


Tx = XBeeDevice("COM5", 9600)
Rx1= RemoteXBeeDevice(Tx, XBee64BitAddress.from_hex_string("0013A200416411DF"))
Rx2= RemoteXBeeDevice(Tx, XBee64BitAddress.from_hex_string("0013A20041630A75")) 
Rx3= RemoteXBeeDevice(Tx, XBee64BitAddress.from_hex_string("0013A200418B68F8"))
Tx.open()

window = tk.Tk()

window.title('LMU AirLions')
#You can set the geometry attribute to change the root windows size
window.geometry("1000x1000") #You want the size of the app to be 500x500

back = tk.Frame(window,bg='black')
window.configure(background='black')

helv46 = font.Font(family='Verdana', size=120)
helv = font.Font(family='Verdana', size= 55)
data_x = 925
data_y = 165

label_x = 825
label_y = 100

helv36 = font.Font(family='Verdana', size=16)
btn_x = 30
btn_y = 740

verd24 = font.Font(family='Verdana', size=24) 


def CDA1():    
    print('servo 1 moved')
    Tx.send_data(Rx1, "hi 1")
    return

def CDA2():    
    print('servo 2 moved')
    Tx.send_data(Rx2, "hi 2")
    return

def CDA3():    
    print('servo 3 moved')
    Tx.send_data(Rx3, "hi 3")
    return
        

CDA1_button = tk.Button(window, text = "CDA1", command = CDA1, font = helv36, height = 2, width = 12, fg = "white", bg = "red", borderwidth = 0)
CDA1_button.pack()

CDA2_button = tk.Button(window, text = "CDA2", command = CDA2, font = helv36, height = 2, width = 12, fg = "white", bg = "blue", borderwidth = 0)
CDA2_button.pack()

CDA3_button = tk.Button(window, text = "CDA3", command = CDA3, font = helv36, height = 2, width = 12, fg = "white", bg = "green", borderwidth = 0)
CDA3_button.pack()

window.mainloop()
Tx.close()
