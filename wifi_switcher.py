# WIFI Switcher als unabhängige exec mit eigenem Zwischenspeicher 
# und GUI


import tkinter as tk
import subprocess


class WifiSwitcher(tk.Tk):
    """Standalone GUI to switch WiFi networks"""
    def __init__(self):
        super().__init__()
        self.title("WiFi Switcher")
        self.geometry("400x250")

        tk.Label(self, text="Enter WiFi SSID: \n or \n Enter Profile Name:", activebackground="lightgrey", activeforeground="cyan").pack(pady=5)
        self.ssid_entry = tk.Entry(self)
        self.ssid_entry.pack(pady=5)

        tk.Label(self, text="(optional) Enter Password:").pack(pady=5)
        self.password_entry = tk.Entry(self)### [, show="*")  ] <-- verstecken ausgeschaltet ###
        self.password_entry.pack(pady=5)

        self.connect_button = tk.Button(self, text="Connect", command=self.connect_to_wifi)
        self.connect_button.pack(pady=10)

        self.status_label = tk.Label(self, text="Status: Not connected", fg="red")
        self.status_label.pack(pady=5)

    def connect_to_wifi(self):
        """Switch to the selected WiFi network"""
        ssid = self.ssid_entry.get()
        password = self.password_entry.get()
        

        if not password:
            password = ""
        if not ssid:
            self.status_label.config(text="Error: SSID (Netztwerkname) benötigt!", fg="red")
            return

                # Test beginn # 
        login = []

        # Windows WiFi command
        command = f'netsh wlan connect name="{ssid}" interface="WLAN"'
        try:
            subprocess.run(command, shell=True, check=True)
            self.status_label.config(text=f"Connected to {ssid}", fg="green")
            stat = "Connected to {ssid}"
        except subprocess.CalledProcessError:
            self.status_label.config(text="Connection Failed", fg="red")
        
if __name__ == "__main__":
    app = WifiSwitcher()
    app.mainloop()
