import tkinter as tk
from tkinter import *
import sys
import datetime
import time
import csv
import tkFont

from dronekit import connect, VehicleMode, Command, LocationGlobal
from pymavlink import mavutil
import math

# Set up import to CSV
global csvtog
csvtog = False
global csvfile
timename = time.strftime('%y-%m-%d___%H_%M_%S')
csvfile = open('SAE_Data_' + timename + '.csv','wb')
thiswriter = csv.writer(csvfile, delimiter = ' ', quoting=csv.QUOTE_MINIMAL)
thiswriter.writerow(['Time:             ' , 'Ground speed:        ', 'Roll:               ', 'Pitch:                  ', 'Altitude:               '])

# Connect to vehicle
connectionString = "com6"
print "Connecting on: ",connectionString
vehicle = connect(connectionString, wait_ready=["groundspeed","attitude","location.global_relative_frame"], baud=57600)

window = tk.Tk()

window.title('LMU AirLions')
#You can set the geometry attribute to change the root windows size
window.geometry("1540x840") #You want the size of the app to be 500x500

back = tk.Frame(window,bg='black')
window.configure(background='black')

# create font sizes
helv120 = tkFont.Font(family='Verdana', size=120)
verd55 = tkFont.Font(family='Verdana', size= 55)
verd24 = tkFont.Font(family='Verdana', size=24)
verd16 = tkFont.Font(family='Verdana', size=16)

# create x and y coordinates
data_x = 1010
data_y = 165
label_x = 925
label_y = 100

# Create button coordinates
btn_x = 30
btn_y = 740

# Create Labels for: altitude, ground speed, latitude, longitude, and clock


# Altitude Label
alt_label = Label(text = "Altitude (ft)", font = verd24, bg = 'black', fg = 'white')
alt_label.place(x=label_x,y=label_y-10)
alt1 = ''
alt2 = Label(window, font = helv120, bg = 'black', fg = 'yellow')
alt2.pack(fill= BOTH, expand = 1)
alt2.place(x=data_x-60, y=label_y+40-10)

# Groundspeed Label
speed_label = Label(text = "Speed (ft/s)", font = verd24 ,bg = 'black', fg = 'white')
speed_label.place(x = label_x+300, y = label_y-10)
speed1 = ''
ground_speed = Label(window, font = helv120, bg = 'black', fg = 'orange')
ground_speed.pack(fill= BOTH, expand = 1)
ground_speed.place(x=data_x+300-40, y=label_y+40-10)

# Distance to Waypoint Label
dest_label = Label(text = "Dist. to WP (ft)", font = verd24, bg = 'black', fg = 'white')
dest_label.place(x=label_x-40, y=label_y+2*180+60+30-20)  
dest1 = ''
waypoint = Label(window, font = verd55, bg = 'black', fg = 'deep sky blue')
waypoint.pack(fill= BOTH, expand = 1)
waypoint.place(x=data_x-50, y=label_y+180+2*60+2*100)

# Latitude Label
lat_label = Label(text = "Latitude", font = verd24, bg = 'black', fg = 'white')
lat_label.place(x = label_x, y=label_y+180+60-10)
lat1 = ''
latitude = Label(window, font = verd55, bg = 'black', fg = 'lime green')
latitude.pack(fill= BOTH, expand = 1)
latitude.place(x= data_x-150, y=label_y+180+65+60-10)

# Longitude Label
long_label = Label(text = "Longitude", font = verd24, bg = 'black', fg = 'white')
long_label.place(x=label_x + 300, y=label_y+180+60-10)
long1 = ''
longitude = Label(window, font = verd55, bg = 'black', fg = 'red2')
longitude.pack(fill= BOTH, expand = 1)
longitude.place(x=data_x+120, y=label_y+180+65+60-10)

# Time Label
global time1
time1 = ''
global clock
clock = Label(window, font=('Verdana', 25), bg='black', fg = 'white')
clock.pack(fill=BOTH, expand=1)
clock.place(x=1175,y=10)

# Main loop gets called every 200ms to update altitude, speed, long, lat, and time
#
#

# Time information
def tick():
    global time1
    global clock
    # get the current local time from the PC
    time2 = time.strftime('%y-%m-%d %H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    getFlightData()
    clock.after(200,tick)
    
# Flight information
def getFlightData():
    groundSpeed = vehicle.groundspeed
    groundSpeed = int(groundSpeed*3.28084)
    roll = vehicle.attitude.roll
    pitch = vehicle.attitude.pitch
    altitude = vehicle.location.global_relative_frame.alt
    altitude = int(altitude*3.28084)

    lat2 = round(vehicle.location.global_frame.lat, 1)
    long2 = round(vehicle.location.global_frame.lon, 1)

    if altitude < 0:    # Dont let the dropTime become imaginary
        altitude = 0

    global csvtog
    if csvtog:
        timeNow = time.strftime('%y-%m-%d %H:%M:%S')
        global csvfile
        thiswriter = csv.writer(csvfile, delimiter = ' ', quoting=csv.QUOTE_MINIMAL)
        thiswriter.writerow([timeNow ,'____', groundSpeed,'_____', altitude])
        
    updateHUD(groundSpeed, roll, pitch, altitude,lat2,long2)
    return (groundSpeed, roll, pitch, altitude,lat2,long2)


def updateHUD(groundSpeed, roll, pitch, altitude,lat2,long2):
    alt2.config(text = altitude)
    ground_speed.config(text = groundSpeed)  
    latitude.config(text = lat2)
    longitude.config(text = long2)
    return
    
# Returns the distance between the current latitude and longitude and where we want to go
def distance():
    lat3 = vehicle.location.global_frame.lat
    long3 = vehicle.location.global_frame.lon

    dest_lat = 33.9692318
    dest_long = -118.4147438
    radius = 3959 * 5280  # km

    dlat = math.radians(dest_lat-lat3)
    dlon = math.radians(dest_long-long3)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat3)) \
        * math.cos(math.radians(dest_lat)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

#updated distance function
def getDistance():
    global dest1
    #(d) = distance()
    d = 0
    if d != dest1:
        dest1 = d
        waypoint.config(text = d)
    waypoint.after(200,getDistance)
    
getDistance()

# create the functions that display which payload was dropped
def CDA():
    CDA_label = Label(text = "CDA", font = ('Verdana', 100), fg = 'white', bg = 'black')
    CDA_label.place(x=100,y=150)
    
    #sets the servos to open the payload 
    vehicle.channels.overrides['7'] = 1500 # right servo
    vehicle.channels.overrides['8'] = 1500 # left servo
    vehicle.flush()
    return

def supply():
    supply_label = Label(text = "Supplies", font = ('Verdana', 100), fg = 'white', bg = 'black')
    supply_label.place(x = 100,y=150)
    
    #sets the servos to open the payload 
    vehicle.channels.overrides['7'] = 1500 # right servo
    vehicle.channels.overrides['8'] = 1500 # leftt servo
    vehicle.flush()
    return        

def habitat():
    habitat_label = Label(text = "Habitat", font = ('Verdana', 100), fg = 'white', bg = 'black')
    habitat_label.place(x=100,y=150)
    
    #sets the servos to open the payload 
    vehicle.channels.overrides['7'] = 1500 
    vehicle.channels.overrides['8'] = 1500 
    vehicle.flush()
    return

# creates a function to reset the servo to its closed position
def reset_servo():
    # reset the servos to close the payload box
    vehicle.channels.overrides['7'] = 2000 
    vehicle.channels.overrides['8'] = 1000 
    vehicle.flush()
    return

# Create button configuration
window.option_add("*Button.Background", "white")
window.option_add("*Button.Foreground", "red")

def toggleCSV():
    global csvtog
    csvtog = not csvtog
    if csvtog:
        #global CSV_button
        CSV_button.config(text = 'Stop Logging')
    else:
        CSV_button.config(text = 'Log Data')
    return

def quitcommand():
    global csvfile
    csvfile.close()
    window.destroy()
    vehicle.close()
    return

# Create buttons to display visuals for payload drops
#
#

# Button for CDA
CDA_button = tk.Button(window, text = "CDA", command = CDA, font = verd16, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
CDA_button.place(x = btn_x, y = btn_y-10)

# Button for Supplies
supply_button = Button(window, text = "Supplies", command = supply, font = verd16, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
supply_button.place(x = btn_x + 185, y = btn_y-10)

# Button for Habitat
habitat_button = Button(window, text = "Habitat", command = habitat, font = verd16, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
habitat_button.place(x = btn_x + 2*185, y = btn_y-10)

# Button to Reset Servos
rst_servo_button = Button(window, text = "Reset Servos", command = reset_servo, font = verd16, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
rst_servo_button.place(x = btn_x+185+100, y = btn_y-110)

# Button for CSV
CSV_button = tk.Button(window, text = "Log Data", command = toggleCSV, font = verd16, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
CSV_button.place(x = btn_x+100, y = btn_y-110)

# Button to Exit
stop = Button(window, text = "Quit", command = quitcommand, font = verd16, height = 2, width = 12, fg = "red", borderwidth = 0, bg = 'grey30')
stop.place(x = btn_x+3*185, y = btn_y-10)

tick()
window.mainloop()
