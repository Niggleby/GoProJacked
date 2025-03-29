import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class TW(tk.Toplevel):
    """A separate window to display script logs/output"""
    def __init__(self, parent):
        super().__init__(parent)
                  #Anfang meiner Testreihe
        tmnl = tk.Toplevel(parent)
        tmnl.title("GoPro Script Output")
        label = tk.Label(tmnl, text="This is the terminal window for script output.") 
        label.pack()
        #Ende der Testreihe  '''
        self.title("Script Output")
        self.geometry("600x400")
        self.resizable(True, True)  # Allow resizing

        # Terminal-style output
        self.text_area = ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED, font=("Courier", 10))
        self.text_area.pack(expand=True, fill=tk.BOTH)

    def log_message(self, message):
        """Append a message to the terminal window"""
        self.text_area.config(state=tk.NORMAL)  # Enable editing
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state=tk.DISABLED)  # Disable editing
        self.text_area.see(tk.END)  # Auto-scroll to bottom
    