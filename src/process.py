from typing import Tuple

import hydra
import pandas as pd
from helpers import load_data, save_data
from omegaconf import DictConfig
from sklearn.model_selection import train_test_split


def get_X_y(data: pd.DataFrame, feature: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Split data into X and y"""
    X = data.drop(columns=feature)
    y = data[feature]
    return X, y


def split_train_test(X: pd.DataFrame, y: pd.Series, test_size: float) -> dict:
    """Split data into train and test sets"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def process_data(config: DictConfig):
    print("Processing the data...")
    df = load_data(config.data.merged.path)
    X, y = get_X_y(df, config.process.feature)
    splitted_datasets = split_train_test(X, y, config.process.test_size)
    for name, data in splitted_datasets.items():
        save_data(data, f"{config.data.processed.dir}/{name}.pkl")


if __name__ == "__main__":
    process_data()
