# Neuer Inhalt: Versuch 2 für WifiManager
# import pywifi  >> maybe später anstatt subprocess
# INFOS: SSID: FRITZNas11144021332; PW: "" ???
# import os
# import time  >>  vllt benötigt fürs warten auf verbindungen

import subprocess
import re       # RegEx [ ^\s*SSID-Name\s*:\s*(.+)$] mit  flags=re.MULTILINE  ==> holt SSID-Name z.b. aus stdout!!

pname = "FRITZNas11144021332"


def check_profile(profile) -> bool:        # '-> bool' definiert Rückgabetyp der Funktion, ist FREIWILLIG
    """Vergleicht eingabe Argument (Profilname = SSID) mit akutell aktivem Profil und gibt bool aus"""
    cp = subprocess.run(
    ["netsh", "wlan", "show", "interfaces", f'profiles', f'name={profile}'],
    capture_output=True,     # stdout/stderr einsammeln
	text=True,               # Dekoaaqefgalirgdiere zu str (statt bytes)
    check=False,             # Fehler nicht automatisch werfen
    timeout=10,               # optional: Abbruch nach 10s
    encoding="utf-8",
    errors="replace"
    )   # wenn cp.returncode = 0 ==> success  \\ es folgt regex-fix Versuch
    vgl = re.search(r"^\s*Profil\s*:\s*(.+)$", cp.stdout, flags=re.MULTILINE).group(1).lower().strip()
    if (cp.returncode == 0):        # bei Erfolg
        # print("success!!")
        return (vgl == profile.lower().strip())
    else:
        print(vgl)
        print(f"FAIIIIIL \nProfilname aus Eingabe (show conn): {profile.lower().strip()}")
        print(cp.stdout)
        return False


#### ==> Try von GPT: ####

def get_current_ssid() -> str | None:
    """listet vorhandene wlan-interfaces und gibt aktuelle !SSID! aus => als return"""
    sp = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if sp.returncode != 0:
        print(f"ERROR -- Returncode nicht null {sp.returncode}")
        return None         # returncode == 0 bedeutet succes! > Hier wird bei Fehlschlag 'None' returned
    # Zeile "SSID : <name>" (nicht BSSID)
    m = re.search(r"^\s*SSID\s*:\s*(.+)$", sp.stdout, flags=re.MULTILINE)
    if not m:
        return f"=========\nKeine Übereinstimmung in folgendem:\n{sp.stdout}\n========="
    ssid = m.group(1).strip()       # ==> .group(n) gibt die n-te matching group an, sollten mehrere existieren & .strip() entfernt leerzeichen vor&nach match
    return ssid if ssid and ssid.upper() != "N/A" else "Stripz nich hoems"



def gp_connect(name="FRITZNas11144021332"):
    """überprüft, ob bereits verbunden, falls nich: Verbindugsaufbau zu GoPro mit OPTIONALER profil/ssid-eingabe"""
    if not check_profile(name):     #    (name.lower().strip() == )
        cnt = subprocess.run(
            ["netsh", "wlan", "connect",f'name={name}', f'ssid={name}'],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
            )
        if cnt.returncode == 0:
            print(f"Erfolgreich verbunden mit: \n{name}\n > {cnt.stdout}")
    else:
        print(f"Bereits verbunden mit: {name}")
# check_profile(pname)
# print(f"SSID aus current ssid: \n{get_current_ssid()}")       # ==> Zeigt Funktionsausgabe (unwicht)
gp_connect()

