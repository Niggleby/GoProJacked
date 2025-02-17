import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class TerminalWindow(tk.Toplevel):
    """A separate window to display script logs/output"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Script Output")
        self.geometry("600x400")

        # Terminal-style output
        self.text_area = ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED, font=("Courier", 10))
        self.text_area.pack(expand=True, fill=tk.BOTH)

    def log_message(self, message):
        """Append a message to the terminal window"""
        self.text_area.config(state=tk.NORMAL)  # Enable editing
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state=tk.DISABLED)  # Disable editing
        self.text_area.see(tk.END)  # Auto-scroll to bottom
