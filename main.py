import os
import json
import shutil
import datetime

import send2trash

timestamp_format = "%Y-%m-%dT%H_%M_%S"
with open("config.json", "r") as f:
    config = json.load(f)

default_target_dir = config["default_target_dir"]
content_sources = config["sources"]

for content in content_sources:
    now = datetime.datetime.utcnow()

    content_path = content["path"]
    now_str = now.strftime(timestamp_format)
    content_label = content["label"]
    nmax_backups = content["nmax_backups"]

    target_root = content.get("target_dir", default_target_dir)
    target_main_dir = os.path.join(target_root, content_label)
    target_dir_version = os.path.join(target_main_dir, now_str)

    shutil.copytree(content["path"], target_dir_version)

    backups_versions = os.listdir(target_main_dir)
    if len(backups_versions) > nmax_backups:
        backups_dates_map = {
            datetime.datetime.strptime(timestamp_str, timestamp_format): timestamp_str
            for timestamp_str in backups_versions
        }
        file_to_remove = backups_dates_map[min(backups_dates_map.keys())]
        send2trash.send2trash(os.path.join(target_main_dir, file_to_remove))
