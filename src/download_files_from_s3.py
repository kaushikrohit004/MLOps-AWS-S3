import os
from pathlib import Path

import boto3
import hydra
from omegaconf import DictConfig


def get_s3_client():
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return s3


def download_data_from_s3(s3, config: DictConfig):
    # Create the local directory if it doesn't exist
    local_directory = Path(config.local_path)
    local_directory.mkdir(parents=True, exist_ok=True)

    # Initialize the S3 bucket object
    objects = s3.list_objects_v2(Bucket=config.bucket, Prefix=config.prefix)

    # List objects
    for obj in objects.get("Contents", []):
        if obj["Key"].endswith(".csv"):
            # Construct the full local file path
            local_file_path = local_directory / Path(obj["Key"]).name

            # Download the file
            s3.download_file(config.bucket, obj["Key"], str(local_file_path))
            print(f"Downloaded {obj['Key']} to {local_file_path}")


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def download_s3_file(config: DictConfig):
    print("Downloading old data from S3...")
    s3 = get_s3_client()
    download_data_from_s3(s3, config.s3.raw.old)


if __name__ == "__main__":
    download_s3_file()
