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
import yaml
#with open("C:/Users/Robin/PyHOME_tst/ProjekteUndRepos/GPJ/GoProJacked/assets/cfgig.yaml", "r") as file:
#    cfgig = yaml.safe_load(file)
#    print(cfgig)

#test zu class#

def get_cfgig():
    """Load configuration from a YAML file"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "cfgig.yaml")
    try: # line entfernt, siehe oben
        with open(config_path, "r") as file:
            cfgig = yaml.safe_load(file)
            # print(cfgig)
        return cfgig
    except yaml.YAMLError as e:
        print("Syntax error in configuration file.")
                        # print("Configuration file not found.")  <-- anderer Fehler

def do_cfgig():
    """Load other configuration from a YAML file"""
    try:
        config_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "cfgig.yaml")
        with open(config_path2, "r") as file2:
            cfgig2 = yaml.safe_load(file2)
            # print(cfgig2)
        return cfgig2
    except yaml.YAMLError as e2:
        print("Syntax error in configuration file.")
                        # print("Configuration file not found.")  <-- anderer Fehler
        return e2
##test zu class ende#

#test zu classabruf#

gcfg = get_cfgig
print(gcfg) 
#
dcfg = do_cfgig()
print(dcfg)

compare = dcfg == gcfg
if compare:
    print("cfgig == dcfg")
else:
    print(gcfg, dcfg)
    print("cfgig  dcfg")
#   print(compare)
###test zu classabruf ende###

if __name__ == "__main__":
    app = GoProApp()
    app.mainloop()