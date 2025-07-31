'''
curl http://localhost:8000/api/schema/?format=openapi -o full_openapi.yaml
python split_openapi.py

'''

# split_openapi.py
import os
import yaml
import json
from collections import defaultdict

MODULES = ["login", "offices", "mapping"]  # 你要切出來的 prefix 模組
INPUT_PATH = "full_openapi.yaml"  # 或 .json
OUTPUT_DIR = "api-doc/src/spec"

def load_openapi_spec(filepath):
    with open(filepath, "r") as f:
        if filepath.endswith(".json"):
            return json.load(f)
        else:
            return yaml.safe_load(f)

def split_spec_by_module(spec, modules):
    grouped = defaultdict(dict)
    for path, details in spec["paths"].items():
        for module in modules:
            if path.startswith(f"/{module}/"):
                grouped[module][path] = details
                break
    return grouped

def write_yaml(output_path, content):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(content, f, sort_keys=False)

def main():
    spec = load_openapi_spec(INPUT_PATH)
    grouped_paths = split_spec_by_module(spec, MODULES)

    for module, paths in grouped_paths.items():
        partial_spec = {
            "openapi": spec["openapi"],
            "info": spec["info"],
            "paths": paths,
            "components": spec.get("components", {}),
        }
        out_file = os.path.join(OUTPUT_DIR, module, "index.yaml")
        write_yaml(out_file, partial_spec)
        print(f"✅ Wrote {len(paths)} paths to {out_file}")

if __name__ == "__main__":
    main()
