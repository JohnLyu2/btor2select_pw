#!/usr/bin/env python3.10

import json
import csv
from pathlib import Path

THIS_SCRIPT_PATH = Path(__file__).resolve()
BTOR2SELECT_DIR = THIS_SCRIPT_PATH.parent
TOOL_DICT_JSON = Path(BTOR2SELECT_DIR) / "tool_config_dict.json"

from main import parse_tool_config

def main():
    with open(TOOL_DICT_JSON, 'r') as f:
        tool_config_dict = json.load(f)
    # convert tool_config_dict key to integer
    tool_config_dict = {int(k): v for k, v in tool_config_dict.items()}
    tool_config_size = len(tool_config_dict)
    return_list = []
    for i in range(tool_config_size):
        return_list.append(parse_tool_config(tool_config_dict[i][1]))
    return_list.sort()
    with open("tool_config_list.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(return_list)

if __name__ == "__main__":
    main()