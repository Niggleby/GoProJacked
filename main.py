import sys
import os
import json
import requests
import tkinter as tk
from tkinter import messagebox

# Füge das GUI-Modul ein (falls nötig)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GoProApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GoPro Controller")
        self.geometry("400x300")

        # JSON-Datei laden
        self.config = self.load_config()

        # Dropdown für HTTP-Befehle
        self.command_var = tk.StringVar(self)
        self.command_var.set(next(iter(self.config.keys())))  # Standardwert (erster Key)

        self.command_menu = tk.OptionMenu(self, self.command_var, *self.config.keys())
        self.command_menu.pack(pady=10)

        # Senden-Button
        self.send_button = tk.Button(self, text="Send Command", command=self.send_command)
        self.send_button.pack(pady=10)

    def load_config(self):
        """Lädt die JSON-Datei als Dictionary."""
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "config.json")
            with open(config_path, "r") as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load config file: {e}")
            return {}

    def send_command(self):
        """Sendet den ausgewählten HTTP-Request."""
        command = self.command_var.get()
        url = self.config.get(command)

        if not url:
            messagebox.showerror("Error", "Invalid command selected.")
            return

        try:
            response = requests.get(url, timeout=5)
            messagebox.showinfo("Response", f"Status: {response.status_code}\n{response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

if __name__ == "__main__":
    app = GoProApp()
    app.mainloop()
