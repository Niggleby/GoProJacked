import tkinter as tk
from tkinter import messagebox
try:     from gopro.goproControl import connect_to_gopro, set_mode, check_connection
# Für nächste klasse -->  try:     from 
except ImportError:
    messagebox.showerror("Import Error", "goproControl module not found. Please ensure it is installed correctly.")
    exit()
from gui.streamWindow import sw
from gui.terminalWindow import TW

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

         #MORE BUTTONSSS!
        self.check_button = tk.Button(self, text="check WIFI", command=self.check_gopro)
        self.check_button.pack(pady=5)

        self.term_button = tk.Button(self, text="open Terminal", command=self.check_gopro)

    def check_gopro(self):
        '''Checks, if Gopro is Wifi-connected'''
        if check_connection():
            messagebox.showinfo("Nice, Connected to")
        else:
            messagebox.showerror("Meh", "läuft nich :C")
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

    def open_terminal_window(self):
        """Opens the terminal window"""
        TW.log_message("This is a test message.")  
        
        
        '''Test 2 über mir X-Zeilen'''