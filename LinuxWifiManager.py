# Linux-Alternative zu WifiManager (netsh)
## IMPORTS ###
import subprocess
import re

### VARS ###

GP_SSID = "FRITZNas11144021332"

### DEFs ###

import subprocess

def get_current_ssid():
    result = subprocess.run(
        ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
        capture_output=True, text=True
    )

    for line in result.stdout.splitlines():
        print(line) # debug
        if line.startswith("yes:"):
            return line.split(":")[1]
        else: print("aktuell Kein WLAN verbunden")
        return None


def check_profile(name:str) -> bool:
    """Prüft ob Eingabestring der SSID des altuellen WLANs entspricht"""
    return get_current_ssid() == name

# ! sicherheitshalber standardname auf bekannte SSID gesetzt, da in Win-WifiManager auch
def gp_connect(name:str, password=None):
    """Verbindet mit WLAN unter Linux (nmcli)"""
    current = get_current_ssid()
    if current == name:
        print(f"Bereits verbunden mit: {name}")
        return

    cmd = ["nmcli", "dev", "wifi", "connect", name]

    if password:
        cmd += ["password", password]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Erfolgreich verbunden mit:\n{name}")
    else:
        print(f"Fehler beim Verbinden:\n{result.stderr}")

### MAIN ###


print(check_profile(GP_SSID))
gp_connect(GP_SSID)


'''
## Linux Commands:
status prüfen:
nmcli -t -f active,ssid dev wifi | grep '^yes'
-> liefert: 'yes:FRITZNas11144021332'

wlan verbinden:
nmcli dev wifi connect "SSID" password "PASSWORT"
-> liefert: 'Error: 802-11-wireless-security.key-mgmt: property is missing.'
!! allerdings OHNE 'password "PASSWORD"'
Passwords or encryption keys are required to access the wireless network 'FRITZNas11144021332'.
Warning: password for '802-11-wireless-security.psk' not given in 'passwd-file' and nmcli cannot ask without '--ask' option.
Device 'wlp4s0' successfully activated with '5aeef5da-6541-4fe2-87f5-a055c53f1911'.
(Vermutlich weil Gerät schonmal verbunden war)
'''