# GoProJacked
simple but powerful http python integration
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "cfgig.yaml") für imports 

---

## Wanted Structure for repo and scripts:
_ehemalige Struktur:_
gopro-http-ui/
│── gui/                # GUI-related files
│   ├── main_window.py  # Main app window
│   ├── stream_window.py # Separate window for GoPro live stream
│   ├── settings_window.py # Camera settings sub-window
│── gopro/              # GoPro API interaction
│   ├── gopro_api.py    # Handles HTTP requests to GoPro  -- macht das Sinn??
│   ├── gopro_control.py # Basic control functions (e.g., connect, set mode)
│── assets/             # Images, icons, etc.
│── main.py             # Entry point of the program
│── requirements.txt    # Dependencies
│── README.md           # Project documentation


### Neue (Ziel-)Struktur:
gopro-http-ui/
│── gui/                # GUI-related files
│   ├── NewGUI.py  # Main app window
│   ├── stream_window.py # Separate window for GoPro live stream
│   ├── stream_setup.py # Camera settings sub-window
│── gopro/              # GoPro API interaction
│   ├── NewMe.py        # Navigiert durch die Request-yaml und 'baut' so commands
│   ├── gopro_control.py # ehem. steuerfunktion (überflüssig)
│── assets/             # Images, icons, etc.
    ├── NewMe.py
    │── MyRequests.yaml     # (Menü-)Struktur der möglichen Command
│── requirements.txt    # Dependencies
│── README.md           # Project documentation
