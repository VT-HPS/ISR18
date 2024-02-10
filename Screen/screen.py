#!/usr/bin/python3
import re
import os
import time
from tkinter import *
from tkinter import ttk
import tkinter as tk
from math import sqrt, pow, pi
from numpy import interp
from pathlib import Path
import threading
import random
from collections import deque

print("hit initial")
gyro_list = [0,0]
depth = 0
speed = 0
depth_value = 0
rpm_value = 0 
rpm_graphic_coord = 0
depth_graphic_coord = 0
depth_indicator = 0


######### CREATE DATALOGGING FILE ###################################################################################

# Create directory if it does not exist
home_dir = os.path.expanduser('~') # Get the path to the user's home directory
directory_path = os.path.join(home_dir, 'HPS/Data/ISR18/')
Path(directory_path).mkdir(parents=True, exist_ok=True)

home_dir = os.path.expanduser('~') # Get the path to the user's home directory
file_path = os.path.join(home_dir, 'HPS/Data/ISR18/serial_list_data.txt') # Create a file path in the home directory
print(file_path)

######### DASHBOARD DISPLAY ITEMS ######################################################################################

# MINOR DISPLAY SETUP ITEMS
root = Tk()  # initialize root variable
root.geometry("800x480")  # root sized to hdmi monitor
root.title('Kraken HUD')

# STYLE CONFIGURATION
root.style = ttk.Style(root)
root.style.configure('title.TLabel', font=('Times', 14, 'bold')) # For gauge labels
root.style.configure('.TLabel', font=('Times', 14)) # gauge readings

# GRID MANAGEMENT (2x3)
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=3)
root.rowconfigure(2, weight=2)

# HEADING DISPLAY SETUP
HEIGHT = 200
WIDTH = 200
RADIUS = 30
TAG = "cir"
# labels
heading_label = ttk.Label(root, text='HEADING', style='title.TLabel', font=("Times", 20, "bold")).grid(column=0, row=0, sticky='n')
heading_up = ttk.Label(root, text='UP', style='.TLabel').grid(column=0, row=1, sticky='n')
heading_port = ttk.Label(root, text='PORT', style='.TLabel').grid(column=0, row=1, sticky='w', padx=100)
heading_starboard = ttk.Label(root, text='STARBOARD', style='.TLabel').grid(column=0, row=1, sticky='e', padx=40)
heading_down = ttk.Label(root, text='DOWN', style='.TLabel').grid(column=0, row=1, sticky='s')
# canvas items
heading_canvas = Canvas(root, width=WIDTH, height=HEIGHT)
heading_canvas.create_line((WIDTH/2)+20, (HEIGHT/2), (HEIGHT/2)-20, (HEIGHT/2))
heading_canvas.create_line((WIDTH/2), (HEIGHT/2)+20, (HEIGHT/2), (HEIGHT/2)-20)
heading_canvas.create_oval((WIDTH/2)-RADIUS, (HEIGHT/2)-RADIUS, (WIDTH/2)+RADIUS,
        (HEIGHT/2)+RADIUS, fill='green', tags=TAG)
heading_canvas.grid(column=0, row=1)

# DEPTH DISPLAY SETUP
# labels
depth_label = ttk.Label(root, text='DEPTH', style='title.TLabel', font=("Times", 25, "bold")).grid(column=1, row=0, sticky='n')
depth_value_label = ttk.Label(root, text="0", style='.TLabel')
depth_value_label.place(x=600, y=45, anchor='n')
# canvas items
depth_canvas = Canvas(root, height=400, width=100)
depth_canvas.create_rectangle(3, 400, 100, 3, width='3')
depth_canvas.grid(column=1, row=1, rowspan=3)
# (x0, y0, x1, y1) = (over 3, down 400, over 100, go down to depth #)
depth_bar = depth_canvas.create_rectangle(3, 400, 100, depth, fill='#FFCC00')


# SPEED DISPLAY SETUP
frame_speed = ttk.Frame(root, padding=10, relief="solid", borderwidth=1)
frame_speed.grid(column=0, row=3, sticky='w', padx=(20, 0), pady=(20, 50))
frame_speed.configure(style="White.TFrame")
style = ttk.Style()
style.configure("White.TFrame", background="white")
label_title = ttk.Label(frame_speed, text="SPEED: ", font=("Times", 25, "bold"))
label_title.grid(column=0, row=0, sticky='w')
label_result = ttk.Label(frame_speed, text="", font=("Times", 60))
label_result.grid(column=1, row=0, sticky='w', padx=(50, 0))


# change color of circle on display according to value
def get_circle_color(x, y, radius):
    #check if coordinate is with in radius of origin
    if radius/2 > int(sqrt( pow(abs(x - (WIDTH/2)), 2) + pow(abs(y - (HEIGHT/2)), 2))): 
        return 'green'
    elif radius * 1.25 < int(sqrt( pow(abs(x - (WIDTH/2)), 2) + pow(abs(y - (HEIGHT/2)), 2))): 
        return 'red'
    else:
        return 'yellow'


# create circle element for display
def create_circle(x, y, r, canvasName, t):
    color = get_circle_color(x,y,r)
    canvasName.create_oval(x-r, y-r, x+r, y+r, fill=color, tags=t)
    root.update()


# delete circle element for display
def delete_circle(canvasName, tag):
    canvasName.delete(tag)
    root.update()



######### INTERPRET PRESSURE SENSOR ######################################################################################

# convert pressure sensor voltage to coordinates for canvas display
def convert_depth_to_coord(depth_value):
    depth_feet = round(depth_value/12)
    #print('depth_feet ', depth_feet)
    if depth_feet >= 30:
        return 3
    elif depth_feet <= 0:
        return 400
    else:
        depth_indicator = interp(depth_feet,[0,30],[400,3])
    return int(depth_indicator)


# calculate depth based on pressure 
def calculate_depth(depth_value):
    depth_feet = round(depth_value/12)
    #print("Depth Value (m) = ", depth_feet)
    return depth_feet


# get speed value    
def display_speed(rpm_value):  
    diameter = 0.0254  # Radius of the rotating object in meters

    rps = rpm_value / 60.0  # Convert RPM to RPS

    circumference = pi * diameter  # Calculate the circumference

    speed = round(circumference * rps, 2)  # Calculate the speed in m/s

    label_result.config(text="{} m/s".format(speed))
    return speed


######### INTERPRET RPM SENSOR ######################################################################################

# convert rpm value to coordinate for display
def convert_rpms_to_coord(data):
    if data >= 250:
        return 550
    elif data <= 0:
        return 3
    else:
        # change these rpm ranges for estimated RPM range
        rpm_indicator = interp(data,[0,250],[3,550])
        return int(abs(rpm_indicator))


######### INTERPRET GYRO SENSOR ######################################################################################

# convert mapped gyro data to coordinates for display
def convert_gyro_to_coord(pitch_value, yaw_value):
    if pitch_value >= 15.0:
        pitch_value = 90
    elif pitch_value <= -15.0:
        pitch_value = -90
    else:
        pitch_value = pitch_value

    if yaw_value > 15.0:
        yaw_value = 90
    elif yaw_value < -15.0:
        yaw_value = -90
    else:
        yaw_value = yaw_value

    y = interp(int(pitch_value/10),[-9,9],[50,150])
    x = interp(int(yaw_value/10),[-9,9],[50,150])
    gyro_list = [int(x), int(y)]
    return gyro_list


######### DISPLAY AND UPDATE DASHBOARD ITEMS ######################################################################################

def gyro_dashboard():
    delete_circle(heading_canvas, TAG)
    create_circle(gyro_list[0], gyro_list[1], RADIUS, heading_canvas, TAG)


# def rpm_dashboard():
#     rpm_graphic_coord = convert_rpms_to_coord(rpm_value)
#     RPM_canvas.coords(RPM_bar, rpm_graphic_coord, 3, 3, 100)
#     #print('rpm_value = ', rpm_value)
#     RPM_value_label.config(text=str(rpm_value))
    

def depth_dashboard():
    global depth
    insideSensorValue = random.randrange(0, 1023) 
    depth = calculate_depth(insideSensorValue)
    depth_graphic_coord = convert_depth_to_coord(insideSensorValue)
    depth_canvas.coords(depth_bar, 3, 400, 100, depth_graphic_coord)
    depth_value_label.config(text=str(depth), font=("Times", 25, "bold"))



def speed_dashboard():
    display_speed(rpm_value)


def update_gui():
    while True:
        gyro_dashboard()
        speed_dashboard()
        #rpm_dashboard()
        depth_dashboard()
        time.sleep(0.1)


def close_win():
   root.destroy()


# FOR TESTING
def get_random_xy_coord():
    global gyro_coord
    global rpm_value
    global depth_indicator
    global ps_value
    global insideSensorValue
    global outsideSensorValue
    global rpm_graphic_coord

    # CREATE A FILE FOR OUTPUTING SERIAL DATA FOR DATALOGGING
    with open(file_path, 'w') as output_file:
        while True:
            time.sleep(0.5)
            data = [random.randrange(-9,9,1), random.randrange(-9,9,1)]
            y = interp(int(data[0]/10),[-9,9],[150,50])
            x = interp(int(data[1]/10),[-9,9],[50,150])
            gyro_coord = [int(x), int(y)]

            rpm_value = random.randrange(0, 250)      
            insideSensorValue = random.randrange(0, 1023) 
            ps_value = random.randrange(12, 360)
            depth_indicator = convert_depth_to_coord(ps_value)
            serial_list = [depth_indicator, rpm_value, int(x), int(y)]
            print('SERIAL LIST ', str(serial_list))
            
            # OUTPUT SERIAL DATA FOR DL
            output_file.write(str(serial_list) + "\n")
            output_file.flush()    
# END OF FOR TESTING



def read_sensor_data():
    global insideSensorValue
    global outsideSensorValue
    global rpm_value
    global speed
    global depth_graphic_coord
    global rpm_graphic_coord
    global gyro_list
    serial_list = []
    serial_list_backup = [0,0,0,0,0,0,0]

    # CREATE A FILE FOR OUTPUTING SERIAL DATA FOR DATALOGGING
    with open(file_path, 'w') as output_file:
        while True:
            serial_list = []
            data = []
            #print('--------------------------------------------')
            #print('incoming serial data: ', data)        
            try: 
                serial_string = (data.decode('ascii'))
            except:
                serial_string = '' 
            serial_string = serial_string.strip()
            serial_string_split = serial_string.split(",")
            #print('serial string split = ', serial_string_split)

            if (data == b'') or (re.match( r'^\.' or r'^\>' or '^\!', serial_string)) :
                serial_list = serial_list_backup.copy()
            else:    
                if "!" not in serial_string.split(","):
                    for x in serial_string.split(","):
                        if x != '': 
                            try:
                                serial_list.append(float(x)) 
                            except:
                                serial_list.append(0)
                        else:
                            serial_list.append(0)
                    
                    if len(serial_list) != 7:
                       serial_list = serial_list_backup.copy()
                    
                    serial_list_backup = serial_list.copy()
                
                else:
                    serial_list = serial_list_backup.copy()
            

            insideSensorValue = serial_list[0]
            depth_graphic_coord = convert_depth_to_coord(insideSensorValue)
            
            outsideSensorValue = serial_list[1]
            
            rpm_value = serial_list[2]
            rpm_graphic_coord = convert_rpms_to_coord(rpm_value)

            pitch_value = serial_list[3]
            yaw_value = serial_list[4]
            gyro_list = convert_gyro_to_coord(pitch_value, yaw_value)
            
            #control_surface_degrees = serial_list[5:]
            #print("Pitch degrees: ", control_surface_degrees[0], ", Yaw degrees: ", control_surface_degrees[1])

            if (data == b'') or (re.match( r'^\.' or r'^\>' or '^\!', serial_string)):
                #print('HIT BACK UP SERIAL LIST')
                continue
            else:
                print('--------------------------------------------')
                print('SERIAL LIST = ', serial_list) 
                print('depth : ', serial_list[0], ' in') 
                print('outsideSensorValue: ', serial_list[1], ' m/s')      
                print('rpm: ', serial_list[2])                 
                print('Yaw value: ', serial_list[3])
                print('Pitch value: ', serial_list[4])


            # OUTPUT SERIAL DATA FOR DL
            output_file.write(str(serial_list) + "\n")
            output_file.flush()  
       

if '__main__' == __name__:
    # heading elements

    # random data testing
    th = threading.Thread(target=get_random_xy_coord, args=(),  daemon=True)

    #th = threading.Thread(target=read_sensor_data, args=(),  daemon=True)
    th.start()
    
    update_gui()

    time.sleep(30)  # Pause for 3 seconds

    #root.mainloop()  # run hud
    #test.mainloop()
