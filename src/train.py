from pathlib import Path

import hydra
import joblib
import pandas as pd
from helpers import load_data
from omegaconf import DictConfig
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def create_pipeline() -> Pipeline:
    return Pipeline([("scaler", StandardScaler()), ("svm", SVC())])


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    pipeline: Pipeline,
    hyperparameters: dict,
    grid_params: dict,
) -> GridSearchCV:
    """Train model using GridSearchCV"""
    grid_search = GridSearchCV(pipeline, dict(hyperparameters), **grid_params)
    grid_search.fit(X_train, y_train)
    return grid_search


def save_model(model, path: str):
    """Save model to path"""
    Path(path).parent.mkdir(exist_ok=True)
    joblib.dump(model, path)


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def train(config: DictConfig) -> None:
    """Train model and save it"""
    print("Training the model...")
    X_train = load_data(f"{config.data.processed.dir}/X_train.pkl")
    y_train = load_data(f"{config.data.processed.dir}/y_train.pkl")
    pipeline = create_pipeline()
    grid_search = train_model(
        X_train,
        y_train,
        pipeline,
        config.train.hyperparameters,
        config.train.grid_search,
    )
    save_model(grid_search.best_estimator_, config.model_path)


if __name__ == "__main__":
    train()
