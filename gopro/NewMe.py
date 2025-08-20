### Idk, is ne experimentelle File oder so, maybe NewMai maan ###
import requests
import yaml
import glob
# import json
import os   # oder shutil
import shutil
# import time

### Variables
profilename = "FRITZNas11144021332"
GOPRO_IP = "10.5.5.9"  # Default GoPro IP when connected via WiFi
gpath = glob.glob('*.yaml')
fname = 'GoProJacked\\assets\\cfgig.yaml'
##fpath = os.path.join(cpath, )
cpath = os.getcwd()
lb = "\n" + "---" * 20 + "\n"
pth = os.path.join(cpath, fname)
###testprint

print(f"Current working directory: {cpath} {lb}")
print(f"Files in current directory: {gpath}{lb}")
print(f"Path to configuration file: {pth}{lb}")

### Load configuration from YAML file
with open(pth, 'r') as file:
    config = yaml.safe_load(file)

print(f"Configuration loaded: {config}{lb}")


###Functions
def connect_to_gopro():
#def goproControl():
    """Check if the GoPro is reachable"""
    try:
        response = requests.get(f"http://{GOPRO_IP}/gp/gpControl")
        return response.status_code == 200
    except requests.ConnectionError:
        return False


 ### Start of request-part ###
    try:
        response = requests.get(f"http://{GOPRO_IP}/gp/gpControl/command/mode?p={mode_mapping[mode]}")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

