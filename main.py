import os
import json
import shutil
import datetime

with open("config.json", "r") as f:
    config = json.load(f)

default_target_dir = config["default_target_dir"]
content_sources = config["sources"]

for content in content_sources:
    now = datetime.datetime.utcnow()

    content_path = content["path"]
    content_name = content_path.split("\\")[-1] + now.strftime("_%Y_%m_%dT%H_%M_%S_UTC")
    content_label = content["label"]

    target_root = content.get("target_dir", default_target_dir)
    target_dir_path = os.path.join(target_root, content_label, content_name)

    shutil.copytree(content["path"], target_dir_path)
