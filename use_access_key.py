import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "access_key.json")

def read_key(json_path):
    with open(json_path, "rt") as rjf:
        json_data = json.load(rjf)
        access_key = json_data["access_key"]
        secret_key = json_data["secret_key"]
        return (access_key, secret_key)
