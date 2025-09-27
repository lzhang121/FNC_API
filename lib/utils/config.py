
import os
import yaml

def load_config(env: str = None):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    env = env or os.getenv("ENV", "test01")
    file_path = os.path.join(base_dir, "config", f"{env}.yaml")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件不存在: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
