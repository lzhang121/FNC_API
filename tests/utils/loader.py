
import os
import yaml

def load_yaml(file_name: str):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir,"data", file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
