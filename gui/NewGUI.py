### TK & CTK Versuch Nr_2 ###


import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import yaml
import requests
import os
import sys
# Hinzufügen des übergeordneten Verzeichnisses zum Pfad
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from WifiManager import get_current_ssid, gp_connect


def send_request(url):
    '''Sendet eine HTTP-GET-Anfrage und zeigt die Antwort an.'''
    try:
        response = requests.get(url, timeout=5)
        msg = f"Status: {response.status_code}\n{response.text[:500]}"
    except Exception as e:
        msg = f"Error: {e}"
    messagebox.showinfo("HTTP Response", msg)


# Load YAML
yaml_path = os.path.join(os.path.dirname(__file__), '../assets/MyRequests.yaml')
with open(yaml_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

app = ctk.CTk()
app.geometry("1200x800")

tabview = ctk.CTkTabview(master=app)
tabview.pack(padx=20, pady=20, fill="both", expand=True)


def add_widgets(parent, node, tab_name=None):
    # Special handling for 'status' tab
    if tab_name == 'status':
        # Add WiFi info and switcher at the top
        wifi_frame = ctk.CTkFrame(parent)
        wifi_frame.pack(fill="x", padx=10, pady=10)
        ssid_var = tk.StringVar()
        def update_ssid():
            ssid = get_current_ssid()
            ssid_var.set(f"Current WiFi: {ssid}")
        update_ssid()
        ssid_label = ctk.CTkLabel(wifi_frame, textvariable=ssid_var, font=("Arial", 13, "italic"))
        ssid_label.pack(anchor="w", pady=2)

        entry_label = ctk.CTkLabel(wifi_frame, text="Switch WiFi (SSID):")
        entry_label.pack(anchor="w", pady=2)
        ssid_entry = ctk.CTkEntry(wifi_frame)
        ssid_entry.pack(anchor="w", pady=2)
        def switch_wifi():
            new_ssid = ssid_entry.get().strip()
            if new_ssid:
                gp_connect(new_ssid)
                update_ssid()
                messagebox.showinfo("WiFi Switch", f"Attempted to switch to: {new_ssid}")
        switch_btn = ctk.CTkButton(wifi_frame, text="Switch", command=switch_wifi)
        switch_btn.pack(anchor="w", pady=2)

    # Continue with normal YAML-driven UI
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, dict):
                frame = ctk.CTkFrame(parent)
                frame.pack(fill="x", padx=10, pady=5)
                label = ctk.CTkLabel(frame, text=key, font=("Arial", 14, "bold"))
                label.pack(anchor="w")
                add_widgets(frame, value)
            else:
                btn = ctk.CTkButton(parent, text=key, command=lambda url=value: send_request(url))
                btn.pack(fill="x", padx=20, pady=4)
    else:
        btn = ctk.CTkButton(parent, text=str(node), command=lambda url=node: send_request(url))
        btn.pack(fill="x", padx=20, pady=4)

# Create a tab for each top-level key
for top_key, top_value in data.items():
    tabview.add(top_key)
    tab = tabview.tab(top_key)
    add_widgets(tab, top_value, tab_name=top_key)

app.mainloop()
