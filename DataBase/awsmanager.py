from os.path import getsize
from pathlib import Path
from typing import Type, Union

import boto3
from ChadUtils.constants import (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
                                 REGION_NAME, TEMP_ROOT)
from ProgressBar.progressbase import IProgressBar


class ChadAWSManager:
    _chad_aws = None

    def __init__(self):
        self._bucket_name = "english-chad"
        
        self._s3_client = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
        ).client('s3')
    
    @classmethod
    def getInstance(cls):
        if cls._chad_aws is None:
            cls._chad_aws = cls()
        return cls._chad_aws

    def uploadFile(self, upload_path: str, callback: Union[Type[IProgressBar], None] = None) -> None:
        with open(TEMP_ROOT.format(Path(upload_path).name), "rb") as file:

            if callback is not None: 
                callback = callback(getsize(
                    TEMP_ROOT.format(Path(upload_path).name)
                )).updateProgress

            self._s3_client.upload_fileobj(
                file, self._bucket_name, upload_path, Callback=callback
            )
        file.close()

    def downloadFile(self, file_path: str, callback: Union[Type[IProgressBar], None] = None) -> None:
        with open(TEMP_ROOT.format(Path(file_path).name), "wb") as file:
            
            if callback is not None: 
                callback = callback(
                    self.getFileHeadData(file_path)
                    .get("ContentLength", 0)
                ).updateProgress
            
            self._s3_client.download_fileobj(
                self._bucket_name, file_path, file, Callback=callback
            )
        file.close()

    def deleteFile(self, file_path: str) -> None:
        self._s3_client.delete_object(
            Bucket=self._bucket_name, Key=file_path,
        )
    
    def getFileHeadData(self, file_path: str) -> dict:
        return self._s3_client.head_object(
            Bucket=self._bucket_name, Key=file_path,
        )
