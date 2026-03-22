### TK & CTK Versuch Nr_2 ###

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import yaml
import json # -> für status-diff
import requests
import os
import sys
from datetime import datetime
import difflib # -> für diff-Ansicht

# Hinzufügen des übergeordneten Verzeichnisses zum Pfad
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

### Unterscheidung Win <-> Linux für entsprechenden WfifManager ###
OS = os.name
print(OS)
if OS == "posix":
    from LinuxWifiManager import get_current_ssid, gp_connect
    print("Linux-OS identifiziert - LinuxWifiManager geladen")
elif OS == "nt":
    from WifiManager import get_current_ssid, gp_connect
    print("Windows-OS identifiziert - WifiManager geladen")
else: print("[ERROR] OS nicht erkannt - kein WifiManager geladen")

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
        status_line = f"Status: {response.status_code}"
        raw_text = response.text
        msg = f"{status_line}\n{raw_text}"
    except Exception as e:
        status_line = "Error"
        raw_text = str(e)
        msg = f"{status_line}: {raw_text}"

    if tab_name == 'status':
        # store in history with timestamp
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_history.append((ts, raw_text))
        if comparison_var.get():
            # append numbered entry to history box
            hb = getattr(status_output_frame, '_history_box', None)
            db = getattr(status_output_frame, '_diff_box', None)
            if hb:
                idx = len(status_history)
                hb.insert("end", f"[{idx}] {ts}\n{raw_text}\n\n")
                hb.see("end")
            # compute diff between first and latest
            if len(status_history) >= 2 and db:
                first = status_history[0][1]
                latest = status_history[-1][1]
                diff_text = compute_diff(first, latest)
                db.delete("1.0", "end")
                db.insert("end", diff_text)
        else:
            # default: replace single status_output_box
            status_output_box.delete("1.0", "end")
            status_output_box.insert("end", msg)
    else:
        messagebox.showinfo("HTTP Response", msg)

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

# Comparison mode control and second textbox (initially hidden)
comparison_var = tk.BooleanVar(value=False)
def toggle_comparison():
    enabled = comparison_var.get()
    if enabled:
        # clear any existing boxes and reset history on (re)activation
        hb_old = getattr(status_output_frame, '_history_box', None)
        db_old = getattr(status_output_frame, '_diff_box', None)
        if hb_old:
            hb_old.place_forget()
            hb_old.destroy()
            delattr(status_output_frame, '_history_box')
        if db_old:
            db_old.place_forget()
            db_old.destroy()
            delattr(status_output_frame, '_diff_box')
        # clear the single-box if present
        try:
            status_output_box.pack_forget()
        except Exception:
            pass
        # reset history
        status_history.clear()
        # create two equally sized boxes using place so they stay equal
        # leave some space at top for the label
        top_rely = 0.12
        box_relheight = 0.42
        padx_rel = 0.02
        status_history_box = ctk.CTkTextbox(status_output_frame)
        status_history_box.place(relx=padx_rel, rely=top_rely, relwidth=1 - 2*padx_rel, relheight=box_relheight)
        status_diff_box = ctk.CTkTextbox(status_output_frame)
        status_diff_box.place(relx=padx_rel, rely=top_rely + box_relheight + 0.02, relwidth=1 - 2*padx_rel, relheight=box_relheight)
        setattr(status_output_frame, '_history_box', status_history_box)
        setattr(status_output_frame, '_diff_box', status_diff_box)
    else:
        # remove split and restore single box
        hb = getattr(status_output_frame, '_history_box', None)
        db = getattr(status_output_frame, '_diff_box', None)
        if hb:
            hb.place_forget()
            hb.destroy()
            delattr(status_output_frame, '_history_box')
        if db:
            db.place_forget()
            db.destroy()
            delattr(status_output_frame, '_diff_box')
        status_output_box.pack(fill="both", expand=True, padx=10, pady=(5,10))

comp_chk = ctk.CTkCheckBox(status_output_frame, text="Comparison mode", variable=comparison_var, command=toggle_comparison)
comp_chk.place(relx=0.5, rely=0.02, anchor="n")

# Storage for history
status_history = []  # list of (timestamp_str, raw_text, parsed_json_or_none)

def try_parse_json(text):
    try:
        import json
        return json.loads(text)
    except Exception:
        return None

def compute_diff(first, latest):
    # If both are dict-like, show keys with different values
    a = try_parse_json(first)
    b = try_parse_json(latest)
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        all_keys = sorted(set(a.keys()) | set(b.keys()))
        for k in all_keys:
            va = a.get(k)
            vb = b.get(k)
            if va != vb:
                diffs.append(f"{k}: {va} -> {vb}")
        return "\n".join(diffs) if diffs else "(no differences)"
    # Fallback: simple line-based diff
    da = first.splitlines(keepends=False)
    db = latest.splitlines(keepends=False)
    diff = difflib.unified_diff(da, db, lineterm='')
    return "\n".join(list(diff)) or "(no differences)"


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
