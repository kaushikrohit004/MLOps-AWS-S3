from pathlib import Path

import hydra
import pandas as pd
from helpers import save_data
from omegaconf import DictConfig


def get_files_in_a_directory(dir_path: str):
    dir_ = Path(dir_path)
    return dir_.glob("*.csv")


def merge_files(csv_files: list):
    print("Merging the following files:")
    dfs = []
    for file in csv_files:
        print(file.name)
        dfs.append(pd.read_csv(file))
    return pd.concat(dfs, ignore_index=True)


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def merge_data(config: DictConfig):
    csv_files = get_files_in_a_directory(config.data.raw.dir)
    merged_df = merge_files(csv_files)
    save_data(merged_df, config.data.merged.path)


if __name__ == "__main__":
    merge_data()
