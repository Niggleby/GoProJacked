### Anfangs übungsdokument für und über Klasse ###m
# import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import yaml
import json
import os

# # # # # # ==> 2 geklaute Funktionen aus <gopro\NewMe.py> 
def load_yaml(path):
    """Lädt eine YAML-Datei und gibt das Dict zurück."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def navigate(data, path):
    """
    Navigiert durch verschachtelte Dicts/Listen.
    path = Liste von Keys, z. B. ["setting", "whitebalance", "6500K"]
    """
    node = data
    for p in path:
        if isinstance(node, dict):
            node = node[p]  # Key auswählen
        elif isinstance(node, list):
            node = node[p]  # Index auswählen
        else:
            raise KeyError(f"Path {path} führt ins Leere.")
    return node
# # # # # #


## Laden + Lesen der Yaml 
filepath = "assets\\MyRequests.yaml"

file = load_yaml(filepath)
nf = navigate(file, ["shutter"])
print(nf)


# '''
mwin = tk.Tk()
mwin.geometry("400x300")
mwin.title("Hauptfenster")

tv = ttk.Treeview(columns="active")
tv.heading("#0", text="Setting")

for k in file:
    #print(f"{k}")
    sname = tv.insert("", tk.END, text=k)
    if isinstance(k, dict):
        for sk in k.items:
            oname = tv.insert('sname', tk.END, text=sk) 
    
# else: 5



tv.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

mwin.mainloop()
# '''