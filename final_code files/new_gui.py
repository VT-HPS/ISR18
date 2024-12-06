import tkinter as tk
from tkinter import ttk
import random
import math

class SpeedDepthHeadingGauges(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HPS HUD")
        self.geometry("600x350")

        # Speed Gauge
        self.speed_frame = tk.Frame(self)
        self.speed_frame.pack(side=tk.LEFT, padx=10)

        self.speed_label = tk.Label(self.speed_frame, text="SPEED", font=("Helvetica", 12))
        self.speed_label.pack(pady=10)

        self.speed_value = tk.StringVar()
        self.speed_value.set("0.0 m/s")

        self.speed_gauge = ttk.Progressbar(self.speed_frame, orient="vertical", length=200, mode="determinate")
        self.speed_gauge.pack(pady=10)

        self.speed_display = tk.Label(self.speed_frame, textvariable=self.speed_value, font=("Helvetica", 16))
        self.speed_display.pack(pady=5)

        # Depth Gauge
        self.depth_frame = tk.Frame(self)
        self.depth_frame.pack(side=tk.RIGHT, padx=10)

        self.depth_label = tk.Label(self.depth_frame, text="DEPTH", font=("Helvetica", 12))
        self.depth_label.pack(pady=10)

        self.depth_value = tk.StringVar()
        self.depth_value.set("0.0 feet")

        self.depth_gauge = ttk.Progressbar(self.depth_frame, orient="vertical", length=200, mode="determinate")
        self.depth_gauge.pack(pady=10)

        self.depth_display = tk.Label(self.depth_frame, textvariable=self.depth_value, font=("Helvetica", 16))
        self.depth_display.pack(pady=5)

        # Heading Gauge (Gyroscope)
        self.heading_frame = tk.Frame(self)
        self.heading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.heading_label = tk.Label(self.heading_frame, text="HEADING", font=("Helvetica", 12))
        self.heading_label.pack(pady=10)

        self.heading_value = tk.StringVar()
        self.heading_value.set("0.0 degrees")

        # self.heading_display = tk.Label(self.heading_frame, textvariable=self.heading_value, font=("Helvetica", 16))
        # self.heading_display.pack(pady=5)

        self.heading_canvas = tk.Canvas(self.heading_frame, width=150, height=150, bg="white")
        self.heading_canvas.pack(pady=10)

        # Schedule the update_random_values function to be called every second
        self.after(1000, self.update_random_values)

    def update_random_values(self):
        # Generate random speed, depth, and heading values
        random_speed = random.uniform(0, 5)
        random_depth = random.uniform(0, 10)
        random_heading = random.uniform(0, 360)

        # Update speed gauge and label
        self.update_speed_gauge(random_speed)

        # Update depth gauge and label
        self.update_depth_gauge(random_depth)

        # Update heading gauge and label
        heading_value = f"{random_heading:.2f} degrees"
        self.heading_value.set(heading_value)

        # Update the heading canvas
        self.update_heading_canvas(random_heading)

        # Schedule the function to be called again after one second
        self.after(1000, self.update_random_values)
        
    def update_speed_gauge(self, new_speed):
        speed_gauge_value = int((new_speed / 5) * 100)
        self.speed_gauge["value"] = speed_gauge_value
        self.speed_value.set(f"{new_speed:.2f} m/s")    
        
    def update_depth_gauge(self, new_depth):
        depth_gauge_value = int((new_depth / 10) * 100)
        self.depth_gauge["value"] = depth_gauge_value
        self.depth_value.set(f"{new_depth:.2f} feet")

    def update_heading_canvas(self, heading_angle):
        # Clear the canvas
        self.heading_canvas.delete("all")

        # Draw background grid
        for angle in range(0, 360, 45):
            x1 = 75 + 60 * math.cos(math.radians(angle))
            y1 = 75 + 60 * math.sin(math.radians(angle))
            x2 = 75 + 70 * math.cos(math.radians(angle))
            y2 = 75 + 70 * math.sin(math.radians(angle))
            self.heading_canvas.create_line(x1, y1, x2, y2)

        # Draw a plus sign in the center
        self.heading_canvas.create_line(70, 75, 80, 75, width=2)
        self.heading_canvas.create_line(75, 70, 75, 80, width=2)

        # Draw the circle indicating the heading
        x = 75 + 60 * math.cos(math.radians(heading_angle))
        y = 75 + 60 * math.sin(math.radians(heading_angle))
        self.heading_canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")

if __name__ == "__main__":
    app = SpeedDepthHeadingGauges()
    app.mainloop()
