import os
import json
import glob
import shutil
import argparse

IMAGE_SUFFIX = ['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF', 'webp', 'WEBP', 'svg', 'SVG']
ignore = ["config.json"]

# Scan the figure directory
def scan(args, config):
    if "max_number" not in config:
        config["max_number"] = 0
    config["emp_number"] = []
    for i in range(config["max_number"]):
        if not glob.glob(os.path.join(args.dir, str(i) + ".*")):
            config["emp_number"].append(i)

# Update the figure directory
def update(args, config):
    # Whether rename picture with consecutive integar
    if args.numeral:
        for root, _, files in os.walk(args.dir):
            for file in files:
                suffix = file.split(".")[-1]
                if suffix in IMAGE_SUFFIX:
                    name = ".".join(os.path.splitext(file)[0:-1])
                    rename = False
                    # Whether to rename
                    if not name.isdigit():
                        rename = True
                    else:
                        number = int(name)
                        if str(number) != name:
                            rename = True
                        if number < 0 or number > config["max_number"]:
                            rename = True
                    
                    # Allocate the new name
                    if rename:
                        if config["emp_number"]:
                            newname = str(config["emp_number"].pop())
                        else:
                            newname = str(config["max_number"])
                            config["max_number"] += 1
                            while(glob.glob(os.path.join(args.dir, newname + ".*"))):
                                newname = str(config["max_number"])
                                config["max_number"] += 1
                        
                        src_path = os.path.join(root, file)
                        dst_path = os.path.join(root, newname + suffix)
                        os.rename(src_path, dst_path)
    
    # 


if __name__=="__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "--api",
        type=str,
        default="https://hotarugali.github.io/Emotions/"
        help="API url of emotions."
    )
    parse.add_argument(
        "--numeral",
        default=False,
        action="store_true",
        help="Whether to renaming picture with consecutive integar."
    )
    parse.add_argument(
        "--dir",
        type=str,
        help="The directory needed to be updated."
    )
    parse.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="The default configuration file under the directory needed to be updated."
    )
    args = parse.parse_args()
    config = {}
    config_path = os.path.join(args.dir, args.config)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)

    scan(args, config)
    update(args, config)

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
    