# GoProJacked
simple but powerful http python integration
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "cfgig.yaml") für imports 

---

## Wanted Structure for repo and scripts:

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



- Dumb Py login delay: (main)
'''
print("GOPRO UI STARTING...")
#wait(1)  # wait for 1 seconds
print("...")
#wait(0.1)  # wait for 5 seconds
print("............")
#wait(2)
print("GOPRO UI STARTED")
'''

