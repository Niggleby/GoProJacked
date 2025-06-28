# new file for terminal window in gui>NewMain_window
## ungetestet 

import tkinter as tk
##vvlt für später|from tkinter import scrolledtext
TW = tk.Tk()  # Create the main window
txtBx = tk.Text(TW, wrap=tk.WORD, bg="lightgrey", fg="black", font=("Arial", 12))  # Create a textbox widget
txtBx.get("1.0", tk.END)  # Get all text from the textbox
txtBx.pack()  # Add the textbox to the window



TW.mainloop()  # Start the GUI event loop