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
from geopy.distance import geodesic


# create global statement to write the instance when payload was released
global payload_drop
payload_drop = ''

# global variables 
global dist_to # distance to target
global dlon    # distance to target (longitude)
global dlat    # distance to target (latitude)

# instantiated global variables
dist_to = 0
dlon = 0
dlat = 0

# Set up import to CSV
global csvtog
csvtog = False
global csvfile

timename = time.strftime('%y-%m-%d___%H_%M_%S')
csvfile = open('SAE_Data_' + timename + '.csv','wb')
thiswriter = csv.writer(csvfile, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
thiswriter.writerow(['Time:' , 'Altitude:', 'Raw Altitude:', 'Groundspeed:', 'Raw Groundspeed:', 'Dist. to Waypoint','Latitude:', 'Longitude:', 'Notes'])


# Connect to Pixhawk (dronekit library)
connectionString = "com6"
print "Connecting on: ",connectionString
vehicle = connect(connectionString, wait_ready=["groundspeed","location.global_relative_frame"], baud=57600)

# downloads commands
cmds = vehicle.commands
cmds.download()
cmds.wait_ready()

window = tk.Tk()

window.title('LMU AirLions')
#You can set the geometry attribute to change the root windows size
window.geometry("1540x840") # change the size of the GUI

# Create button configuration
window.option_add("*Button.Background", "white")
window.option_add("*Button.Foreground", "red")

back = tk.Frame(window,bg='black')
window.configure(background='black')

# create font sizes
helv120 = tkFont.Font(family='Verdana', size=120)
verd55 = tkFont.Font(family='Verdana', size= 55)
verd24 = tkFont.Font(family='Verdana', size=24)
verd16 = tkFont.Font(family='Verdana', size=16)
verd = tkFont.Font(family='Verdana', size=14)

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
alt_label.place(x=label_x+100,y=label_y-10)
alt1 = ''
alt2 = Label(window, font = helv120, bg = 'black', fg = 'yellow')
alt2.pack(fill= BOTH, expand = 1)
alt2.place(x=data_x+40, y=label_y+30)

# Groundspeed Label
speed_label = Label(text = "Speed (ft/s)", font = verd24 ,bg = 'black', fg = 'white')
speed_label.place(x = label_x+350, y = label_y-10)
speed1 = ''
ground_speed = Label(window, font = helv120, bg = 'black', fg = 'orange')
ground_speed.pack(fill= BOTH, expand = 1)
ground_speed.place(x=data_x+310, y=label_y+30)

# Distance to Waypoint Label
dest_label = Label(text = "Dist. to WP (ft)", font = verd24, bg = 'black', fg = 'white')
dest_label.place(x = label_x+150, y=label_y+230)
dest1 = ''
waypoint = Label(window, font = verd55, bg = 'black', fg = 'deep sky blue')
waypoint.pack(fill= BOTH, expand = 1)
waypoint.place(x= data_x+100, y=label_y+180+65+60-10)

# Latitude Label
lat_label = Label(text = "Latitude", font = verd16, bg = 'black', fg = 'white')
lat_label.place(x = label_x, y=label_y+180+60-10+200)
lat1 = ''
latitude = Label(window, font = verd, bg = 'black', fg = 'lime green')
latitude.place(x= data_x-150+30, y=label_y+180+60-10+200+60)

# Longitude Label
long_label = Label(text = "Longitude", font = verd16, bg = 'black', fg = 'white')
long_label.place(x = label_x+10+300,  y=label_y+180+60-10+200)
long1 = ''
longitude = Label(window, font = verd, bg = 'black', fg = 'red2')
longitude.place(x=data_x+10+200+30, y=label_y+180+60-10+200+60)

# Target Longitude
cur_long_label = Label(text = "Target Long -118.4812373", font = verd, bg = 'black', fg = 'white')
cur_long_label.place(x=data_x+10+200+30, y=label_y+180+60-10+200+100)

# Target Latitude
cur_lat_label = Label(text = "Target Lat 34.1753158", font = verd, bg = 'black', fg = 'white')
cur_lat_label.place(x=data_x+10+200+60-400, y=label_y+180+60-10+200+100)

# Time Label
global time2
time2 = ''
global clock
clock = Label(window, font=('Verdana', 25), bg='black', fg = 'white')
clock.pack(fill=BOTH, expand=1)
clock.place(x=1175,y=10)


# Main loop gets called every 200ms to update altitude, speed, long, lat, and time
#
#
# Time information
def tick():
    global time2
    global clock
    # get the current local time from the PC
    time1 = time.strftime('%y-%m-%d %H:%M:%S')
    # if time string has changed, update it
    if time1 != time2:
        time2 = time1
        clock.config(text=time1)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    getFlightData()
    clock.after(200,tick)

# Returns the distance between the current latitude and longitude and where we want to go
def distance():
    # call back the global variable
    global dist_to

    lat3 = vehicle.location.global_frame.lat  # current latitude coordinates
    long3 = vehicle.location.global_frame.lon # current longitude coordinates

    # Destination coordinates
    dest_lat = 34.175297
    dest_long = -118.481256

    global dlon
    global dlat

    dlat = (dest_lat-lat3)*363918
    dlon = (dest_long-long3)*303099
    
    # used the following code to compare lateral and longitude results with the previous lines
    # of code
    """
    print "current latitude" lat3
    print "distance between the current latitude coordinate and target coordinate" dlat
    print "distance between the current longitude coordinate and target coordinate" dlon
    a = math.sqrt(dlat*dlat+dlon*dlon)
    """
    # create a compass heading 
    
    # NORTHWEST
    if (dlon > 20 and dlat > 20 ):
        compass_label = Label(text = "NW", font = verd55, bg = 'black', fg = 'white')
        compass_label.place(x = 800, y = 300)
    # NORTH
    elif(dlon > 20 and dlat < 20 and dlat > -20):
        compass_label = Label(text = "N", font = verd55, bg = 'black', fg = 'white')
        compass_label.place(x = 800, y = 300)
    # NORTHEAST
    elif(dlon > 20 and dlat < -20):
        compass_label = Label(text = "NE", font = verd55, bg = 'black', fg = 'white')
        compass_label.place(x = 800, y = 300)
    # WEST
    elif(dlon < 20 and dlon > -20 and dlat > 20):
        compass_label = Label(text = "W", font = verd55, bg = 'black', fg = 'white')
        compass_label.place(x = 800, y = 300)
    # SOUTHEAST
    elif(dlon < -20 and dlat < -20):
        compass_label = Label(text = "SE", font = verd55, bg = 'black', fg = 'white')
        compass_label.place(x = 800, y = 300)
    # SOUTH
    elif(dlon < -20 and dlat > -20 and dlat < 20):
        compass_label = Label(text = "S", font = verd55, bg = 'black', fg = 'white')
        compass_label.place(x = 800, y = 300)
    # SOUTHWEST
    elif(dlon < -20 and dlat > 20):
        compass_label = Label(text = "SW", font = verd55, bg = 'black', fg = 'white')
        compass_label.place(x = 800, y = 300)
    # EAST
    elif(dlon < -20 and dlon < 20 and dlat < -20):
        compass_label = Label(text = "E", font = verd55, bg = 'black', fg = 'white')
        compass_label.place(x = 800, y = 300)

    # this is from the geodesic python library which was more accurate
    # than using pythagorean theorem    
    current_loc = (vehicle.location.global_frame.lat, vehicle.location.global_frame.lon) # current coordinates
    target_loc = (34.175297, -118.481256) # target coordinates
    a = geodesic(current_loc, target_loc).feet
    dist_to = a
    dist_to = int(dist_to)
    return (dist_to) # return the distance calculated

# Updates the distance readings and label
def getDistance():
    global dest1
    global dist_to
    dist_to = distance()
    if dist_to != dest1:
        dest1 = dist_to
        waypoint.config(text = dist_to)
    waypoint.after(300,getDistance)
distance()    
getDistance()

# Flight information
def getFlightData():
    groundSpeed = vehicle.groundspeed
    groundSpeed = int(groundSpeed*3.28084)
    altitude = vehicle.location.global_relative_frame.alt
    altitude = int(altitude*3.28084)

    if altitude < 0:
        altitude = -1
    
    # Prevents from losing connection and losing readings
    try:
        global x3 # temp latitude
        global y3 # temp longitude
        global a1 # temp altitude
        global g1 # temp groundpeed
        
        a1 = altitude
        g1 = groundSpeed

        lat2 = vehicle.location.global_frame.lat
        x3 = lat2
        long2 = vehicle.location.global_frame.lon
        y3 = long2
    except:
        altitude = a1
        groundSpeed = g1
        lat2 = x3
        long2 = y3

    global csvtog
    if csvtog:
        timeNow = time.strftime('%y-%m-%d %H:%M:%S')
        global csvfile
        global dist_to
        thiswriter = csv.writer(csvfile, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
        dist_to = distance()
        thiswriter.writerow([timeNow, int(vehicle.location.global_relative_frame.alt*3.28084), vehicle.location.global_relative_frame.alt*3.28084, int(vehicle.groundspeed*3.2804),vehicle.groundspeed*3.28084, dist_to, vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, payload_drop])
        
    updateHUD(groundSpeed, altitude)
    return (groundSpeed, altitude)

def updateHUD(groundSpeed, altitude):
    alt2.config(text = altitude)
    ground_speed.config(text = groundSpeed)
    global dlon
    global dlat
    latitude.config(text = dlon)
    longitude.config(text = dlat)

    return

# create the functions that display which payload was dropped
def CDA():
    CDA_label = Label(text = "CDA", font = ('Verdana', 100), fg = 'white', bg = 'black')
    CDA_label.place(x=40,y=175)

    CDA_alt = int(vehicle.location.global_relative_frame.alt*3.28084)
    if CDA_alt < 0:
        CDA_alt = 0
    
    CDA_alt_label = Label(text = CDA_alt, font = ('Verdana', 100), fg = 'yellow', bg = 'black')
    CDA_alt_label.place(x=129,y=350)    

    global csvfile
    global dist_to

    timeNow = time.strftime('%y-%m-%d %H:%M:%S')
    payload_drop = "CDAs were dropped"
    thiswriter = csv.writer(csvfile, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
    thiswriter.writerow([timeNow, int(vehicle.location.global_relative_frame.alt*3.28084), vehicle.location.global_relative_frame.alt*3.28084, int(vehicle.groundspeed*3.2804),vehicle.groundspeed*3.28084, dist_to, vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, payload_drop])

    # channel 6 connects to 2 servos for releasing the CDAs
    vehicle.channels.overrides['6'] = 2500
    return
    
def supply():
    supply_label = Label(text = "Supplies", font = ('Verdana', 100), fg = 'white', bg = 'black')
    supply_label.place(x = 400,y=10)
    habitat_label = Label(text = "Habitats", font = ('Verdana', 100), fg = 'white', bg = 'black')
    habitat_label.place(x = 400,y=175)
   
    supply_alt = int(vehicle.location.global_relative_frame.alt*3.28084)
    if supply_alt < 0:
        supply_alt = 0

    supply_alt_label = Label(text = supply_alt, font = ('Verdana', 100), fg = 'yellow', bg = 'black')
    supply_alt_label.place(x=600,y=350)      
    
    global csvfile
    global dist_to
    timeNow = time.strftime('%y-%m-%d %H:%M:%S')
    payload_drop = "Supplies and habitats were dropped!"
    thiswriter = csv.writer(csvfile, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
    thiswriter.writerow([timeNow, int(vehicle.location.global_relative_frame.alt*3.28084), vehicle.location.global_relative_frame.alt*3.28084, int(vehicle.groundspeed*3.2804),vehicle.groundspeed*3.28084, dist_to, vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, payload_drop])

    # side door servos
    vehicle.channels.overrides['8'] = 1257
    vehicle.channels.overrides['5'] = 1500
    return
 
# creates a function to reset the servo to its closed position
def reset_servo():  
    vehicle.channels.overrides['5'] = 2500
    vehicle.channels.overrides['6'] = 905 
    vehicle.channels.overrides['8'] = 500
    return

def show_entry_fields():    
    if (int(servo_ch.get()) == int(3)):
        vehicle.channels.overrides['3'] = int(servo_pos.get())
    elif (int(servo_ch.get()) == int(5)):
        vehicle.channels.overrides['5'] = int(servo_pos.get())
    elif (int(servo_ch.get()) == int(6)):
        vehicle.channels.overrides['6'] = int(servo_pos.get())
    elif (int(servo_ch.get()) == int(7)):
        vehicle.channels.overrides['7'] = int(servo_pos.get())
    elif (int(servo_ch.get()) == int(8)):
        vehicle.channels.overrides['8'] = int(servo_pos.get())

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

# Button for CDA
CDA_button = tk.Button(window, text = "CDA", command = CDA, font = verd16, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
CDA_button.place(x = btn_x, y = btn_y-10)

# Button for Supplies
supply_button = Button(window, text = "Supplies/Habitats", command = supply, font = verd16, height = 2, width = 18, fg = "white", borderwidth = 0, bg = 'grey30')
supply_button.place(x = btn_x + 185, y = btn_y-10)

# Button to Reset Servos
rst_servo_button = Button(window, text = "Reset Servos", command = reset_servo, font = verd16, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
rst_servo_button.place(x = btn_x+185+90-60-30, y = btn_y-110)

# Button for CSV
CSV_button = tk.Button(window, text = "Log Data", command = toggleCSV, font = verd16, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
CSV_button.place(x = btn_x, y = btn_y-110)

# Button to Exit
stop = Button(window, text = "Quit", command = quitcommand, font = verd16, height = 2, width = 12, fg = "red", borderwidth = 0, bg = 'grey30')
stop.place(x = btn_x+2*185+80, y = btn_y-10)

# label for the channel input
servo_ch_label = Label(window, text="Channel", font = ('Verdana', 15), fg = 'white', bg = 'black')
servo_ch_label.place(x=600-170, y = 590)

# label for the position input
pos_servo_label = Label(text = "Position", font = ('Verdana', 15), fg = 'white', bg = 'black')
pos_servo_label.place(x=570, y=590)

# enter the channel corresponding to the servo you want to move
servo_ch = Entry(window, justify = CENTER)
servo_ch.place(x=410, y=630)

#enter the servo position
servo_pos = Entry(window, justify = CENTER)
servo_pos.place(x=550, y = 630)

enter_btn = Button(window, text = "Set Servo", height = 2, width = 15, font = 10, command=show_entry_fields, fg = 'white', bg = 'grey30',borderwidth = 0)
enter_btn.place(x = 470, y = 660)

tick()
window.mainloop()
