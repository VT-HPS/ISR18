import tkinter as tk
from tkinter import ttk
import random
import math
from numpy import interp
import time
import globals
import queue

class SpeedDepthHeadingGauges(tk.Tk):
    def __init__(self, sensor_data_queue):
        super().__init__()

        self.sensor_data_queue = sensor_data_queue
        self.data = None
        
        default_background_color = self.cget("bg")
        
        self.title("HPS HUD")
        self.geometry("800x480")

        # Speed Gauge
        self.speed_frame = tk.Frame(self)
        self.speed_frame.pack(side = tk.LEFT, padx = 10)

        self.speed_label = tk.Label(self.speed_frame, text = "SPEED", font = ("Helvetica", 12))
        self.speed_label.pack(pady = 10)

        self.speed_value = tk.StringVar()
        self.speed_value.set("0.0 m/s")

        self.speed_gauge = ttk.Progressbar(self.speed_frame, orient = "vertical", length = 200, mode = "determinate")
        self.speed_gauge.pack(pady = 10)

        self.speed_display = tk.Label(self.speed_frame, textvariable = self.speed_value, font = ("Helvetica", 16))
        self.speed_display.pack(pady = 5)

        # Depth Gauge
        self.depth_frame = tk.Frame(self)
        self.depth_frame.pack(side = tk.RIGHT, padx = 10)

        self.depth_label = tk.Label(self.depth_frame, text = "DEPTH", font = ("Helvetica", 12))
        self.depth_label.pack(pady=10)

        self.depth_value = tk.StringVar()
        self.depth_value.set("0.0 feet")

        self.depth_canvas = tk.Canvas(self.depth_frame, width = 50, height = 300, background = default_background_color, highlightthickness = 1, highlightbackground = "black")
        self.depth_canvas.pack(pady=10)

        self.depth_display = tk.Label(self.depth_frame, textvariable = self.depth_value, font = ("Helvetica", 16))
        self.depth_display.pack(pady=5)

        # Heading Gauge (Gyroscope)
        self.gauge_frame = tk.Frame(self)
        self.gauge_frame.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

        self.heading_label = tk.Label(self.gauge_frame, text = "HEADING", font = ("Helvetica", 12))
        self.heading_label.grid(row = 0, column = 0) 
         
        self.rpm_value = tk.StringVar()
        self.rpm_value.set("RPM:   0.0")
        
        self.rpm_label = tk.Label(self.gauge_frame, font = ("Helvetica", 12), textvariable = self.rpm_value)
        self.rpm_label.grid(row=0, column=1)

        self.heading_value = tk.StringVar()
        self.heading_value.set("0.0 degrees")

        self.heading_canvas = tk.Canvas(self.gauge_frame, width=200, height=200, background = default_background_color, highlightthickness = 1, highlightbackground = "black")
        self.heading_canvas.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.rpm_canvas = tk.Canvas(self.gauge_frame, width = 200, height = 200, background = default_background_color)
        self.rpm_canvas.grid(row = 1, column = 1, padx = 10, pady = 10)

        # Battery Warning
        self.battery_warning_label = tk.Label(self, text = "", font=("Helvetica", 16), fg = "red")
        self.battery_warning_label.pack()

        # Voltage monitoring variables
        self.voltage = 13.0  # Initial simulated voltage
        self.low_voltage_time = 0  # Timer for low voltage warning
        
        # Standby Overlay
        self.standby = tk.Frame(self, bg = "red", width = 600, height = 300)
        self.standby_label = tk.Label(self.standby, text = "STANDBY", fg = "white", bg = "red", font = ("Arial", 40))
        self.standby_label.pack(pady = 20)

        # Schedule the update_random_values function to be called every second
        #self.after(1000, self.update_random_values(sensor_data_queue))
        self.update_random_values()

    # If voltage < 12 for more than 3 seconds then it shows the warning, hides otherwise
    def check_battery_voltage(self):
        if self.voltage < 12:
            self.low_voltage_time += 1
            if self.low_voltage_time >= 3:
                self.show_battery_warning()
        else:
            self.low_voltage_time = 0
            self.hide_battery_warning()
    
    def show_battery_warning(self):
        self.battery_warning_label.config(text = "⚠️ Battery Low!")

    def hide_battery_warning(self):
        self.battery_warning_label.config(text = "")

    def update_random_values(self):
        # Show standby screen
        if globals.gui_show_standby:
            self.show_standby()
        else:
            # TESTING CODE FOR QUEUE
            try:
                data = self.sensor_data_queue.get_nowait()
                print(f"new data: {data}")
                self.data = data
            except queue.Empty:
                print("queue is empty")
                data = self.data
                pass
            
            
            self.hide_standby()
        
            # Generate random speed, depth, and heading values
            #random_speed = random.uniform(0, 5)
            #random_depth = random.uniform(0, 30)
            random_heading = random.uniform(0, 360)
            #random_rpm = random.uniform(0, 200) # placeholder max rpm

            # Update speed gauge and label
            #self.update_speed_gauge(random_speed)
            self.update_speed_gauge(data["pressure_speed"])

            # Update depth gauge and label
            #self.update_depth_gauge(random_depth)
            self.update_depth_gauge(data["depth"])

            # Update heading gauge and label
            heading_value = f"{random_heading:.2f} degrees"
            self.heading_value.set(heading_value)

            # Update the heading canvas
            self.update_heading_canvas(random_heading)
            
            # Update rpm gauge
            #self.update_rpm_gauge(random_rpm)
            self.update_rpm_gauge(data["rpm"])

            # Simulated voltage between 10 and 14 volts
            #self.voltage = random.uniform(10, 14)  
            self.voltage = data["battery_voltage"]

        # Check battery voltage
        self.check_battery_voltage()
        
        # Schedule the function to be called again after one second
        self.after(1000, self.update_random_values)
        
    def update_speed_gauge(self, new_speed):
        speed_gauge_value = int((new_speed / 5) * 100)
        self.speed_gauge["value"] = speed_gauge_value
        self.speed_value.set(f"{new_speed:.2f} m/s")    
        
    def update_depth_gauge(self, new_depth):
        self.depth_canvas.delete("all")

        max_depth = 30
        goal_depth = 15

        # Calculate bubble position
        depth_height = int((new_depth / max_depth) * self.depth_canvas.winfo_height())
        goal_height = int((goal_depth / max_depth) * self.depth_canvas.winfo_height())

        # Draw the bubble indicating current depth
        self.depth_canvas.create_rectangle(2, depth_height - 5, 50, depth_height + 5, fill = "red", outline = "red")

        # Draw the green square indicating the goal point
        self.depth_canvas.create_rectangle(2, goal_height - 5, 50, goal_height + 5, outline = "green", width = 2)
        
        # Draw some labels on the depth bar
        self.depth_canvas.create_text(7, 10, text = "0")
        self.depth_canvas.create_text(13, self.depth_canvas.winfo_height() / 4, text = str(max_depth * 0.25))
        self.depth_canvas.create_text(17, (self.depth_canvas.winfo_height() / 4) * 3, text = str((max_depth * 0.75)))
        self.depth_canvas.create_text(11, self.depth_canvas.winfo_height() - 10, text = str(max_depth))
        
        self.depth_value.set(f"{new_depth:.2f} feet")

    def update_heading_canvas(self, heading_angle):
        # Clear the canvas
        self.heading_canvas.delete("all")

        # Draw background grid 
        for angle in range(0, 360, 45):
            x1 = (self.heading_canvas.winfo_width() // 2) + 60 * math.cos(math.radians(angle))
            y1 = (self.heading_canvas.winfo_height() // 2) + 60 * math.sin(math.radians(angle))
            x2 = (self.heading_canvas.winfo_width() // 2) + 70 * math.cos(math.radians(angle))
            y2 = (self.heading_canvas.winfo_height() // 2) + 70 * math.sin(math.radians(angle))
            self.heading_canvas.create_line(x1, y1, x2, y2)

        # Draw a plus sign in the center
        half_height = (self.heading_canvas.winfo_height() // 2)
        half_width = (self.heading_canvas.winfo_width() // 2)
        self.heading_canvas.create_line(half_height + 10, half_width, half_height - 10, half_width, width=2)
        self.heading_canvas.create_line(half_height, half_width + 10, half_height, half_width - 10, width=2)

        # Draw the circle indicating the heading
        x = 75 + 60 * math.cos(math.radians(heading_angle))
        y = 75 + 60 * math.sin(math.radians(heading_angle))
        self.heading_canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")
        
    def update_rpm_gauge(self, new_value: str): # current placeholder max rpm is 200
        # Clear the canvas
        self.rpm_canvas.delete("all")
        
        # draw the circle
        half_height = (self.rpm_canvas.winfo_height() // 2)
        half_width = (self.rpm_canvas.winfo_width() // 2)
        self.rpm_canvas.create_oval(2, 2, self.rpm_canvas.winfo_width() - 2, self.rpm_canvas.winfo_height() - 2, width=2)
        self.rpm_canvas.create_line(0, half_height, half_width * 2, half_height, width = 2)
        
        # use interp to get the right angle for the rpm, draw the corresponding line
        angle = interp(new_value,[0,200],[0,180]) # MAX RPM ON THIS LINE. CURRENTLY 200. PLACEHOLDER
        x = half_width - half_width * math.cos(math.radians(angle))
        y = half_height - half_height * math.sin(math.radians(angle))
        self.rpm_canvas.create_line(half_width, half_height, x, y, width = 3, fill = "red")
        
        # create labels for the rpm value
        new_value = round(new_value, 2)
        self.rpm_value.set(f"RPM:   {new_value}")
        self.rpm_canvas.create_text(half_width, half_height + half_height / 2, text = new_value, font = ("Helvetica 30"))
        
        # draw number labels for rpm gauge. CURRENT VALUES ARE PLACEHOLDERS
        self.rpm_canvas.create_text(10, half_height - 10, text = "0", font = ("Helvetica 10")) # left
        self.rpm_canvas.create_text(half_width, 15, text = "100", font = ("Helvetica 10")) # top
        self.rpm_canvas.create_text(half_width * 2 - 20, half_height - 10, text = "200", font = ("Helvetica 10")) # right
        
    def show_standby(self): # show the standby message on top of screen
        self.standby.lift()
        self.standby.place(relx = 0.5, rely = 0.5, anchor = 'center')

    def hide_standby(self): # hide standby screen
        self.standby.place_forget()  # Remove the overlay from view


# TODO REMOVE THIS FOR FINAL VERSION
#if __name__ == "__main__":
    #app = SpeedDepthHeadingGauges()
    #app.mainloop()