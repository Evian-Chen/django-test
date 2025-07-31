import os
import yaml
import json
from collections import defaultdict

# 可調整：你的 Django App 名稱（會對應 URL prefix）
MODULES = ["users", "clubs", "auth"]

# 可調整：你的完整 OpenAPI 輸入檔案位置
INPUT_PATH = "openapi.yaml"

# 可調整：每個 module 的文件會放在哪裡
OUTPUT_DIR = "api-doc/src/spec"

def load_openapi_spec(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        if filepath.endswith(".json"):
            return json.load(f)
        return yaml.safe_load(f)

def match_module(path, module):
    clean = path.lstrip("/")
    return clean.startswith(module + "/") or f"/{module}/" in path

def split_spec_by_module(spec, modules):
    grouped = defaultdict(dict)
    for path, details in spec.get("paths", {}).items():
        for module in modules:
            if match_module(path, module):
                grouped[module][path] = details
                break
    return grouped

def write_yaml(output_path, content):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(content, f, sort_keys=False, allow_unicode=True)

def main():
    spec = load_openapi_spec(INPUT_PATH)
    grouped_paths = split_spec_by_module(spec, MODULES)

    for module, paths in grouped_paths.items():
        if not paths:
            continue
        partial_spec = {
            "openapi": spec.get("openapi", "3.0.0"),
            "info": spec.get("info", {}),
            "paths": paths,
            "components": spec.get("components", {}),
        }
        out_file = os.path.join(OUTPUT_DIR, module, "index.yaml")
        write_yaml(out_file, partial_spec)
        print(f"✅ Wrote {len(paths)} paths to {out_file}")

if __name__ == "__main__":
    main()
