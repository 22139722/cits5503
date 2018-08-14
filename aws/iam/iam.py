from botocore.exceptions import ClientError
from django.conf import settings
from django.utils import timezone
from lib.models import AWSCommandResponse
from lib.utils import boto_client, boto_resource, DictOfLists
from pprint import pprint, pformat
import pytz


tz = pytz.timezone(settings.TIME_ZONE)


# direct boto3 calls
def get_user(username):
    iam_client = boto_client('iam')
    response = iam_client.get_user(UserName=username)
    AWSCommandResponse.objects.create(
        command='get_user',
        response=pformat(response, indent=4)
    )
    return response.get('User')


def list_users(path_prefix='/CITS5503'):
    iam_client = boto_client('iam')
    response = iam_client.list_users(PathPrefix=path_prefix)
    return response


# process boto3 calls
def get_users_list(path_prefix='/CITS5503'):
    response = list_users(path_prefix)
    users = response.get('Users', [])
    return {'Users': users}


def get_active_users_list(path_prefix='/CITS5503'):
    response = list_users(path_prefix)
    users = response.get('Users', [])
    active_users = []
    for user in users:
        password_last_used = user.get('PasswordLastUsed', None)
        if password_last_used is not None:
            active_users.append(user)

    return {'Users': active_users}


def get_inactive_users_list(path_prefix='/CITS5503'):
    response = list_users(path_prefix)
    users = response.get('Users', [])
    inactive_users = []
    for user in users:
        password_last_used = user.get('PasswordLastUsed', None)
        if password_last_used is None:
            inactive_users.append(user)

    return {'Users': inactive_users}


def delete_inactive_users(path_prefix='/CITS5503'):
    iam_client = boto_client('iam')
    iam_resource = boto_resource('iam')
    cloud_computing_group = iam_resource.Group('CloudComputing')

    inactive_users = get_inactive_users_list(path_prefix)
    responses = DictOfLists()
    for user in inactive_users['Users']:
        # response[user.get('UserName')] = 'deleted'

        username = user.get('UserName')

        try:
            responses.add(username, cloud_computing_group.remove_user(UserName=username))
        except ClientError as e:
            responses.add(username, str(e))

        try:
            responses.add(username, iam_client.delete_login_profile(UserName=username))
        except ClientError as e:
            responses.add(username, str(e))

        try:
            response = iam_client.list_access_keys(UserName=username)
            keys = response.get('AccessKeyMetadata', [])
            for key in keys:
                access_key_id = key.get('AccessKeyId', '')
                responses.add(username, iam_client.delete_access_key(UserName=username, AccessKeyId=access_key_id))
        except Exception as e:
            responses.add(username, str(e))

        try:
            responses.add(username, iam_client.delete_user(UserName=username))
        except ClientError as e:
            responses.add(username, str(e))

    return responses


def update_user_path(username, new_path):
    iam_client = boto_client('iam')
    response = iam_client.update_user(UserName=username, NewPath=new_path)
    AWSCommandResponse.objects.create(
        command='update_user',
        response=pformat(response, indent=4),
    )


