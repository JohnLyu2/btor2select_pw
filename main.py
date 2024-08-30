#!/usr/bin/env python3.10

import sys
import json
from pathlib import Path

THIS_SCRIPT_PATH = Path(__file__).resolve()
BTOR2SELECT_DIR = THIS_SCRIPT_PATH.parent
LOCAL_PIPS_DIR = BTOR2SELECT_DIR / "lib"
SAVED_MODEL_DIR = BTOR2SELECT_DIR / "pw_xg_par2_0826"
TOOL_DICT_JSON = Path(BTOR2SELECT_DIR) / "tool_config_dict.json"
sys.path.append(str(LOCAL_PIPS_DIR))

import numpy as np
import joblib
import xgboost as xgb

from create_btor2kw import generate_btor2kw


class PairwiseXGBoost(xgb.XGBClassifier):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fit(self, X, y, weights):
        super().fit(X, y, sample_weight=weights)
        return self


def parse_tool_config(tool_config):
    parts = tool_config.split(".")
    if len(parts) >= 2:
        return (parts[0], parts[1])
    raise ValueError(f"Invalid tool configuration: {tool_config}")


def get_pw_algorithm_selection_lst(btor2_path, model_matrix, random_seed=0):
    btor2kw = generate_btor2kw(btor2_path)
    btor2kw_array = np.array(btor2kw).reshape(1, -1)
    config_size = model_matrix.shape[0]
    votes = np.zeros(config_size, dtype=int)
    for i in range(config_size):
        for j in range(i + 1, config_size):
            prediction = model_matrix[i, j].predict(btor2kw_array)
            if prediction[0]:  # i is better
                votes[i] += 1
            else:
                votes[j] += 1
    np.random.seed(random_seed)
    random_tiebreaker = np.random.random(config_size)
    structured_votes = np.rec.fromarrays(
        [votes, random_tiebreaker], names="votes, random_tiebreaker"
    )
    sorted_indices = np.argsort(structured_votes, order=("votes", "random_tiebreaker"))[
        ::-1
    ]
    return sorted_indices


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {THIS_SCRIPT_PATH} <btor2_path>")
        return
    btor2_path = sys.argv[1]
    if not Path(btor2_path).is_file():
        print(f"The provided btor2 file does not exist: {btor2_path}")
        return
    with open(TOOL_DICT_JSON, "r") as f:
        tool_config_dict = json.load(f)
    # convert tool_config_dict key to integer
    tool_config_dict = {int(k): v for k, v in tool_config_dict.items()}
    tool_config_size = len(tool_config_dict)
    model_matrix = np.empty((tool_config_size, tool_config_size), dtype=object)
    model_matrix[:] = None
    for i in range(tool_config_size):
        for j in range(i + 1, tool_config_size):
            model_matrix[i, j] = joblib.load(SAVED_MODEL_DIR / f"xg_{i}_{j}.joblib")
    selected_lst = get_pw_algorithm_selection_lst(btor2_path, model_matrix)
    selected_id = selected_lst[0]
    selected_tool_config = tool_config_dict[selected_id][1]
    print(parse_tool_config(selected_tool_config))


if __name__ == "__main__":
    main()
