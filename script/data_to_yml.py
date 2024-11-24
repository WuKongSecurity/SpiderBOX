import os
import yaml


def read_existing_data(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print("Error reading existing YAML file:", e)
        return None