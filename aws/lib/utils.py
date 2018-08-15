import boto3
from django.conf import settings


class DictOfLists:

    def __init__(self):
        self.dict = {}

    def add(self, key, value):
        if key in self.dict:
            self.dict[key].append(value)
        else:
            self.dict[key] = [value]


def boto_client(service_name):
    return boto3.client(service_name, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID, region_name=settings.AWS_REGION)


def boto_resource(service_name):
    return boto3.resource(service_name, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID, region=settings.AWS_REGION)
