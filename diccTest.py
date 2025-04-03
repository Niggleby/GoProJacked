# Dateianfang 
import sys
import os
import _tkinter as tk  
# from tkinter import __all__   # --> überrekation von mir?
from tkinter import messagebox   # --> überrekation von mir?
import yaml
import requests

# Folgendes nur falls nötig,
# da schon in main enthalten:

### sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ### -> Bitte nur bei Fehler implementieren und hoffen lol

# Und jetzt erstmal Fensterchen bauen:

        ## PLACEHOLDER TK ##
#
#
#
        
        ## PLACEHOLDER END ##

# GUI-Prozess und master-window entwerfen / aussuchen"

class KaKu(tk.Tk):              # What does that exactly do?
    def __init__(self):         # Knew a man, whom I asked the same Question:
        super().__init__() 
        
        self.title("KaKu's Guckloch in die TKinterferien")
        self.geometry("500x500")
    #   self.__annotations__.__dict__(ipo)    <-- für später keep
    #  
## Connect Button
        self.connect_button = tk.Button(self, text="Connect to GoPro", command=self.connect)
        self.connect_button.pack(pady=10)


# YAML-Import:


if __name__ == "__main__":
    app = KaKu()
    app.mainloop()
else:
    app = KaKu()
    app.mainloop()