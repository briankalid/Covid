import boto3
import botocore

from core.settings import settings
from schemas.file_filter import FileFilterSchema

class s3Controller:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def upload_file(self, file, country, year):
        filename = f"{country}_{year}.csv"
        # print(filename)
        print("cc",file,"asdas")
        self.s3.upload_fileobj(file.file, f"{country.lower()}-bucket-covidkalid", filename)
        print("exito")


    def list_buckets(self):
        return self.s3.list_buckets()
    
    def file_exist(self,bucket, key):
        try:
            self.s3.head_object(Bucket=bucket, Key=key)
            return True
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False

    def get_list_files_by_filter(self,query_params: FileFilterSchema):
        query_params = query_params.model_dump(exclude_unset=True, exclude_defaults=True)
        print(query_params)
        if query_params["all"]:
            for country in settings.COUNTRIES:
                bucket = f"{country.lower()}-bucket-covidkalid"
                print(bucket) 
                objects = self.s3.list_objects(
                    Bucket=bucket)
        else:
            bucket = query_params.get("bucket",None)
            objects = self.s3.list_objects(
                    Bucket=bucket)
            
        return objects


s3controller = s3Controller()