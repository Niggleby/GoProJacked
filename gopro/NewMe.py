import yaml
import requests
import json


def load_yaml(path):
    """Lädt eine YAML-Datei und gibt das Dict zurück."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def navigate(data, path):
    """
    Navigiert durch verschachtelte Dicts/Listen.
    path = Liste von Keys, z. B. ["setting", "whitebalance", "6500K"]
    """
    node = data
    for p in path:
        if isinstance(node, dict):
            node = node[p]  # Key auswählen
        elif isinstance(node, list):
            node = node[p]  # Index auswählen
        else:
            raise KeyError(f"Path {path} führt ins Leere.")
    return node

def gp_send(data, path):
        """Analog zu navigate() mit autom. requesten"""
        url = navigate(data, path)
        r = requests.get(url)
        r_json = r.json()
        r_cont = r.content
        r_error = r.raise_for_status
        r_scode = r.status_code
        if r_scode == 200:
            if isinstance(r_json, dict):
                print(f"Request success!\n{json.dumps(r_json, indent=4 ,ensure_ascii=True)}")
            elif not r_json:
                print(f"Request success!\n{r_scode}\n >Type: {type(r_scode)}")
            else:
                print(f"Request success!\n{r_json}\n {type(r_json)}")
        else: print(f"Request FAILED\n{r_error}")




# Beispielverwendung
if __name__ == "__main__":
    data = load_yaml("assets/MyRequests.yaml")

    # Status-URL holen
# print(navigate(data, ["status"]))
    # -> http://10.5.5.9/gp/gpControl/status

gp_send(data, ["settings", "protune", "active", "is_on"])
'''
    # Shutter ON
    print(navigate(data, ["shutter", "on"]))
    # -> http://10.5.5.9/gp/gpControl/command/shutter?p=1

    # Whitebalance 6500K
    print(navigate(data, ["setting", "whitebalance", "6500K"]))
    # -> http://10.5.5.9/gp/gpControl/setting/11/3
'''