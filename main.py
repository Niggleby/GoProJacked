'''
print("GOPRO UI STARTING...")
#wait(1)  # wait for 1 seconds
print("...")
#wait(0.1)  # wait for 5 seconds
print("............")
#wait(2)
print("GOPRO UI STARTED")
'''

## Wanted Structure for repo and scripts:
'''
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
'''


import sys
import os
import requests

# Add the parent directory to the sys.path to ensure the gui module can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.main_window import GoProApp

if __name__ == "__main__":
    app = GoProApp()
    app.mainloop()