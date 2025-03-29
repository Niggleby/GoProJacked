import requests

GOPRO_IP = "10.5.5.9"  # Default GoPro IP when connected via WiFi

def connect_to_gopro():
#def goproControl():
    """Check if the GoPro is reachable"""
    try:
        response = requests.get(f"http://{GOPRO_IP}/gp/gpControl")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def set_mode(mode):
    """Change the GoPro mode"""
    mode_mapping = {
        "video": 0,
        "photo": 1,
        "timelapse": 2
    }
    

    if mode not in mode_mapping:
        return False

    try:
        response = requests.get(f"http://{GOPRO_IP}/gp/gpControl/command/mode?p={mode_mapping[mode]}")
        return response.status_code == 200
    except requests.ConnectionError:
        return False
