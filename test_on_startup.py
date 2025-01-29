import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Test Window")

# Set window size
root.geometry("300x150")

# Create a bright label
label = tk.Label(root, text="FILE IS RUNNING!", fg="red", bg="yellow", font=("Arial", 16, "bold"))
label.pack(expand=True, fill="both")

# Run the Tkinter event loop
root.mainloop()
