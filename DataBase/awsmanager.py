import boto3


class ChadAWSManager:
    _chad_aws = None

    def __new__(cls, *args, **kwargs):
        if cls._chad_aws is None:
            cls._chad_aws = super().__new__(cls, *args, **kwargs)
        return cls._chad_aws
    
    def __init__(self):
        self._bucket_name = "english-chad"
        self._s3_client = boto3.Session(
            aws_access_key_id="AKIAZTAFQGAI3TCYD4PL",
            aws_secret_access_key="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",
            region_name="eu-central-1",
        ).client('s3')
    
    def uploadFile(self, file, upload_path) -> None:
        self._s3_client.upload_fileobj(
            file, self._bucket_name, upload_path
        )
    
    def downloadFile(self, file, file_path):
        self._s3_client.download_fileobj(
            self._bucket_name, file_path, file
        )
        return file
    
    def deleteFile(self, file_path) -> None:
        self._s3_client.delete_object(
            Bucket=self._bucket_name, 
            Key=file_path,
        )
