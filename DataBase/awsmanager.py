from pathlib import Path

import boto3
from ChadUtils.constants import (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
                                 REGION_NAME, TEMP_ROOT)


class ChadAWSManager:
    _chad_aws = None

    def __new__(cls, *args, **kwargs):
        if cls._chad_aws is None:
            cls._chad_aws = super().__new__(cls, *args, **kwargs)
        return cls._chad_aws

    def __init__(self):
        self._bucket_name = "english-chad"
        self._s3_client = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
        ).client('s3')

    def uploadFile(self, upload_path) -> None:
        with open(TEMP_ROOT.format(Path(upload_path).name), "rb") as file:
            self._s3_client.upload_fileobj(file, self._bucket_name, upload_path)
        file.close()

    def downloadFile(self, file_path) -> None:
        with open(TEMP_ROOT.format(Path(file_path).name), "wb") as file:
            self._s3_client.download_fileobj(self._bucket_name, file_path, file)
        file.close()

    def deleteFile(self, file_path) -> None:
        self._s3_client.delete_object(
            Bucket=self._bucket_name,
            Key=file_path,
        )