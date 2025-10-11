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

''' Alte methode - kurz pausiert
def send_request(url):
    Sendet eine HTTP-GET-Anfrage und zeigt die Antwort an.
    try:
        response = requests.get(url, timeout=5)
        msg = f"Status: {response.status_code}\n{response.text[:500]}"
    except Exception as e:
        msg = f"Error: {e}"
    messagebox.showinfo("HTTP Response", msg)
'''

# Neue Testmethode:
def send_request(url, tab_name=None):
    '''Sendet eine HTTP-GET-Anfrage und zeigt die Antwort an.'''
    try:
        response = requests.get(url, timeout=5)
        msg = f"Status: {response.status_code}\n{response.text}"
    except Exception as e:
        msg = f"Error: {e}"
    if tab_name == 'status':
        status_output_box.delete("1.0", "end")
        status_output_box.insert("end", msg)
    else:
        # messagebox.showinfo("HTTP Response", msg)
        status_output_box.insert("\n", [{url}], {msg})

# Load YAML
yaml_path = os.path.join(os.path.dirname(__file__), '../assets/MyRequests.yaml')    
with open(yaml_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

app = ctk.CTk()
app.geometry("1200x800")

tabview = ctk.CTkTabview(master=app)
tabview.pack(padx=20, pady=20, fill="both", expand=True)




# Rechte Fensterseite definieren für statusoutput (Output area for status response)
status_output_frame = ctk.CTkFrame(app)
# Place the frame below the tabview (tabview is packed with pady=20)
status_output_frame.place(relx=0.53, rely=0.07, relwidth=0.45, relheight=0.91)
# Center the label above the textbox
status_output_label = ctk.CTkLabel(status_output_frame, text="Status Output:", font=("Arial", 14, "bold"), justify="center")
status_output_label.pack(anchor="n", pady=(10, 0))
status_output_box = ctk.CTkTextbox(status_output_frame)
status_output_box.pack(fill="both", expand=True, padx=10, pady=(5, 10))


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
                btn = ctk.CTkButton(parent, text=key, command=lambda url=value: send_request(url, tab_name=tab_name))
                btn.pack(fill="x", padx=20, pady=4)
    else:
        btn = ctk.CTkButton(parent, text=str(node), command=lambda url=node: send_request(url, tab_name=tab_name))
        btn.pack(fill="x", padx=20, pady=4)

# Create a tab for each top-level key



def create_scrollable_tab(tab, node, tab_name=None):
    # Set background color to match CTkFrame, ensure valid Tk color string
    raw_bg = None
    if hasattr(ctk, 'ThemeManager') and 'CTkFrame' in ctk.ThemeManager.theme:
        raw_bg = ctk.ThemeManager.theme['CTkFrame']['fg_color']
    if isinstance(raw_bg, (list, tuple)):
        bg_color = raw_bg[0]  # Use first color if tuple/list
    elif isinstance(raw_bg, str):
        bg_color = raw_bg
    else:
        bg_color = '#2b2b2b'  # fallback

    # Create a canvas and scrollbar inside the tab
    canvas = tk.Canvas(tab, bg=bg_color, highlightthickness=0)
    canvas.place(relx=0, rely=0, relwidth=0.5, relheight=1)
    scrollbar = ctk.CTkScrollbar(tab, orientation="vertical", command=canvas.yview)
    scrollbar.place(relx=0.5, rely=0, relwidth=0.03, relheight=1)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    inner_frame = ctk.CTkFrame(canvas)
    inner_frame_id = canvas.create_window((0, 0), window=inner_frame, anchor="nw", width=int(app.winfo_width()*0.5))


    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(inner_frame_id, width=canvas.winfo_width())
        # Fill remaining space below content with background color
        canvas_height = canvas.winfo_height()
        frame_height = inner_frame.winfo_height()
        if frame_height < canvas_height:
            canvas.create_rectangle(0, frame_height, canvas.winfo_width(), canvas_height, fill=bg_color, outline="")
    inner_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_frame_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    add_widgets(inner_frame, node, tab_name=tab_name)

for top_key, top_value in data.items():
    tabview.add(top_key)
    tab = tabview.tab(top_key)
    create_scrollable_tab(tab, top_value, tab_name=top_key)

app.mainloop()
