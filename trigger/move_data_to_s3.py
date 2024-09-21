import os

import boto3
import hydra
from dotenv import load_dotenv
from omegaconf import DictConfig

load_dotenv()


def get_s3_client():
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return s3


def upload_to_s3(s3, config: DictConfig):
    with open(config.local_path, "rb") as file:
        s3.put_object(Body=file, Bucket=config.bucket, Key=config.object_key)

    print(
        f"File {config.local_path} uploaded to S3 bucket {config.bucket}/{config.object_key}"
    )


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def move_data_to_s3(config: DictConfig):
    s3 = get_s3_client()
    upload_to_s3(s3, config.s3.raw.new)


if __name__ == "__main__":
    move_data_to_s3()
