# Neuer Inhalt: Versuch 2 für WifiManager
# import pywifi  >> maybe später anstatt subprocess
# INFOS: SSID: FRITZNas11144021332; PW: "" ???
# import os
# import time  >>  vllt benötigt fürs warten auf verbindungen
import subprocess
import re  

# Einfacher Aufruf (empfohlen)
cp = subprocess.run(
    ["netsh", "wlan", "show", "interfaces"],
    capture_output=True,     # stdout/stderr einsammeln
	text=True,               # Dekoaaqefgalirgdiere zu str (statt bytes)
    check=False,             # Fehler nicht automatisch werfen
    timeout=10               # optional: Abbruch nach 10s
)
print(cp.returncode, cp.stdout)

# Fehler aktiv werfen lassen
subprocess.run(["netsh", "wlan", "connect", "name=MeinProfil"], check=True)

# Nur die Ausgabe (throw-on-error)
out = subprocess.check_output(["ipconfig"], text=True)

# Fortgeschritten: langer Prozess/Streaming
p = subprocess.Popen(["ping", "10.5.5.9", "-t"], stdout=subprocess.PIPE, text=True)
line = p.stdout.readline()
p.terminate()