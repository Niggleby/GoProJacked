import tkinter as tk
from tkinter import messagebox
try:
    from gopro.gopro_control import connect_to_gopro, set_mode
    ImportError:
        messagebox.showerror("Import Error", "gopro_control module not found. Please ensure it is installed correctly.")
        self.quit()
    self.quit()
from stream_window import sw

class GoProApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GoPro Controller")
        self.geometry("400x300")

        # Connect Button
        self.connect_button = tk.Button(self, text="Connect to GoPro", command=self.connect)
        self.connect_button.pack(pady=10,)

        # Mode Selection
        self.mode_var = tk.StringVar(value="video")
        self.mode_menu = tk.OptionMenu(self, self.mode_var, "video", "photo", "timelapse")
        self.mode_menu.pack(pady=10)

        # Set Mode Button
        self.set_mode_button = tk.Button(self, text="Set Mode", command=self.set_mode)
        self.set_mode_button.pack(pady=10)

        # Open Stream Button
        self.stream_button = tk.Button(self, text="Open Stream Window", command=self.open_stream_window)
        self.stream_button.pack(pady=10)

    def connect(self):
        """Connect to the GoPro via WiFi"""
        if connect_to_gopro():
            messagebox.showinfo("Success", "Connected to GoPro!")
        else:
            messagebox.showerror("Error", "Failed to connect.")

    def set_mode(self):
        """Set the camera mode"""
        mode = self.mode_var.get()
        if set_mode(mode):
            messagebox.showinfo("Success", f"Mode set to {mode}!")
        else:
            messagebox.showerror("Error", "Failed to set mode.")

    def open_stream_window(self):
        """Opens the stream window"""
        sw.open_stream()
