import os
import time
from tkinter import *
from tkinter import ttk
import tkinter as tk
import threading


#######################################################################################################
################################################ SETUP ################################################
#######################################################################################################

######### CREATE DATALOGGING FILE #####################################################################

home_dir = os.path.expanduser('~')
directory_path = os.path.join(home_dir, 'HPS/Data/ISR18/')
os.makedirs(directory_path, exist_ok=True)

home_dir = os.path.expanduser('~')
file_path = os.path.join(home_dir, 'HPS/Data/ISR18/serial_list_data.txt')
print(file_path)

#######################################################################################################
############################################## DASHBOARD ##############################################
#######################################################################################################

######### Overall Display #############################################################################

root = Tk()
root.geometry("800x480")
root.title('Kraken HUD')

# STYLE CONFIGURATION
root.style = ttk.Style(root)
root.style.configure('title.TLabel', font=('Times', 14, 'bold'))  # For gauge labels
root.style.configure('.TLabel', font=('Times', 14))  # Gauge readings

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=5)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=5)
root.rowconfigure(2, weight=1)

canvas_top = tk.Canvas(root, height=70, width=800, bg='white', highlightthickness=0) 
canvas_bottom = tk.Canvas(root, height=70, width=570, bg='white', highlightthickness=0)

canvas_middle_left = tk.Canvas(root, height=410, width=115, bg='white', highlightthickness=0)
canvas_middle_middle = tk.Canvas(root, height=340, width=570, bg='white', highlightthickness=0)
canvas_middle_right = tk.Canvas(root, height=410, width=115, bg='white', highlightthickness=0)

# Placing in grid
canvas_top.grid(row=0, column=0, columnspan=3, sticky='NSEW') 
canvas_bottom.grid(row=2, column=1, sticky='NSEW')

canvas_middle_left.grid(row=1, column=0, rowspan=2, sticky='NSEW')
canvas_middle_middle.grid(row=1, column=1, sticky='NSEW')
canvas_middle_right.grid(row=1, column=2, rowspan=2, sticky='NSEW')

######### Alert Message Display (Canvas Top) ##########################################################

# height=70, width=800

# Coordinates for the rectangle
alert_rect_x1, alert_rect_y1, alert_rect_x2, alert_rect_y2 = 0, 0, 800, 70

# Create the rectangle with a black outline
canvas_top.create_rectangle(alert_rect_x1, alert_rect_y1, alert_rect_x2, alert_rect_y2, outline='black', width=2, fill='white')

# Initial text for the label
alert_text = "Centered Text"
# Calculate the center of the rectangle
center_x = (alert_rect_x1 + alert_rect_x2) / 2
center_y = (alert_rect_y1 + alert_rect_y2) / 2

# Create the label and center it within the rectangle
alert_label_top = tk.Label(canvas_top, text=alert_text, font=('Times', 20))
alert_label_top.place(x=center_x, y=center_y, anchor='center')

######### Status Display (Canvas Bottom) ##############################################################

# height=70, width=570

# Coordinates for the rectangle
status_rect_x1, status_rect_y1, status_rect_x2, status_rect_y2 = 0, 0, 570, 70

# Create the rectangle with a black outline
canvas_bottom.create_rectangle(status_rect_x1, status_rect_y1, status_rect_x2, status_rect_y2, outline='black', width=2, fill='white')

# Initial text for the label
status_text = "Centered Text"
# Calculate the center of the rectangle
center_x = (status_rect_x1 + status_rect_x2) / 2
center_y = (status_rect_y1 + status_rect_y2) / 2

# Create the label and center it within the rectangle
status_label_bottom = tk.Label(canvas_bottom, text=status_text, font=('Times', 20))
status_label_bottom.place(x=center_x, y=center_y, anchor='center')

######### RPM Display (Canvas Middle Right) ##############################################################

# height=410, width=115

# Coordinates for the rectangle
rpm_rect_x1, rpm_rect_y1, rpm_rect_x2, rpm_rect_y2 = 0, 0, 115, 340

# Create the rectangle with a black outline
canvas_middle_right.create_rectangle(rpm_rect_x1, rpm_rect_y1, rpm_rect_x2, rpm_rect_y2, outline='black', width=2, fill='white')

# Initial text for the label
rpm_text = "RPM: ???"
# Calculate the center of the rectangle
center_y = rpm_rect_y2 + (70 / 2)
center_x = (rpm_rect_x1 + rpm_rect_x2) / 2

# Create the label and center it within the rectangle
rpm_label_right = tk.Label(canvas_middle_right, text=rpm_text, font=('Times', 14))
rpm_label_right.place(x=center_x, y=center_y, anchor='center')

######### RPM Display (Canvas Middle Right) ##############################################################

# height=410, width=115

# Coordinates for the rectangle
depth_rect_x1, depth_rect_y1, depth_rect_x2, depth_rect_y2 = 0, 0, 115, 340

# Create the rectangle with a black outline
canvas_middle_left.create_rectangle(depth_rect_x1, depth_rect_y1, depth_rect_x2, depth_rect_y2, outline='black', width=2, fill='white')

# Initial text for the label
depth_text = "Depth: ???"
# Calculate the center of the rectangle
center_y = depth_rect_y2 + (70 / 2)
center_x = (depth_rect_x1 + depth_rect_x2) / 2

# Create the label and center it within the rectangle
depth_label_left = tk.Label(canvas_middle_left, text=depth_text, font=('Times', 14))
depth_label_left.place(x=center_x, y=center_y, anchor='center')

######### Heading Display (Canvas Middle Middle) ##############################################################

# height=340, width=570

# Coordinates for the rectangle
depth_rect_x1, depth_rect_y1, depth_rect_x2, depth_rect_y2 = 0, 0, 115, 340

# Create the rectangle with a black outline
# Draw horizontal rectangle
canvas_middle_middle.create_rectangle(0, 110, 570, 230, outline='black', width=2)

# Draw vertical rectangle
canvas_middle_middle.create_rectangle(220, 0, 340, 340, outline='black', width=2)

# Draw rectangle for the hollow inside
canvas_middle_middle.create_rectangle(220, 110, 340, 230, outline='white', fill='white', width=2)

if '__main__' == __name__:
    root.mainloop()  # Run the HUD
    
