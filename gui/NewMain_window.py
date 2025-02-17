# Update für Terminalserver in main window
## ungetestet

import tkinter as tk
from tkinter import messagebox
from gui.stream_window import open_stream
from gui.terminal_window import TerminalWindow
from gopro.gopro_control import connect_to_gopro, set_mode

class GoProApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GoPro Controller")
        self.geometry("400x300")

        # Open Terminal Button
        self.terminal_window = None
        self.terminal_button = tk.Button(self, text="Open Terminal", command=self.open_terminal)
        self.terminal_button.pack(pady=10)

        # Connect Button
        self.connect_button = tk.Button(self, text="Connect to GoPro", command=self.connect)
        self.connect_button.pack(pady=10)

        # Mode Selection
        self.mode_var = tk.StringVar(value="video")
        self.mode_menu = tk.OptionMenu(self, self.mode_var, "video", "photo", "timelapse")
        self.mode_menu.pack(pady=10)

        # Set Mode Button
        self.set_mode_button = tk.Button(self, text="Set Mode", command=self.set_mode)
        self.set_mode_button.pack(pady=10)

        # Open Stream Button
        self.stream_button = tk.Button(self, text="Open Stream Window", command=open_stream)
        self.stream_button.pack(pady=10)

    def open_terminal(self):
        """Opens the terminal window for script output"""
        if self.terminal_window is None or not self.terminal_window.winfo_exists():
            self.terminal_window = TerminalWindow(self)
        else:
            self.terminal_window.lift()

    def connect(self):
        """Connect to the GoPro via WiFi"""
        status = connect_to_gopro()
        if self.terminal_window:
            self.terminal_window.log_message(f"Connecting to GoPro... {'Success' if status else 'Failed'}")

        if status:
            messagebox.showinfo("Success", "Connected to GoPro!")
        else:
            messagebox.showerror("Error", "Failed to connect.")

    def set_mode(self):
        """Set the camera mode"""
        mode = self.mode_var.get()
        status = set_mode(mode)
        if self.terminal_window:
            self.terminal_window.log_message(f"Setting mode to {mode}... {'Success' if status else 'Failed'}")

        if status:
            messagebox.showinfo("Success", f"Mode set to {mode}!")
        else:
            messagebox.showerror("Error", "Failed to set mode.")

if __name__ == "__main__":
    app = GoProApp()
    app.mainloop()
