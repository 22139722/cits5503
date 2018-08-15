from botocore.exceptions import ClientError
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from lib.models import AWSCommandResponse
from lib.utils import boto_client, boto_resource, DictOfLists
from pprint import pprint, pformat
import pytz


def get_instances():
    current_time = timezone.now().astimezone(timezone.utc)

    ec2_client = boto_client('ec2')
    response = ec2_client.describe_instances()
    reservations = response.get('Reservations')

    all_instances = []

    for reservation in reservations:
        instances = reservation.get('Instances')
        for instance in instances:
            state = instance.get('State', {}).get('Name')
            launch_time = instance.get('LaunchTime')
            up_time = current_time - launch_time if state == 'running' else timezone.timedelta(hours=0)
            instance['UpTime'] = up_time
            instance['Old'] = up_time > timezone.timedelta(hours=12)
            instance['NoKey'] = instance.get('KeyName', '') == ''
            instance['NonWhitelistedInstanceType'] = instance.get('InstanceType') not in settings.AWS_INSTANCE_TYPE_WHITELIST
            
        all_instances += instances
        
    return all_instances
    

def get_old_instances():
    instances = get_instances()
    return [i for i in instances if i['Old']]


def get_young_instances():
    instances = get_instances()
    return [i for i in instances if not i['Old']]


def get_instances_for_termination():
    instances = get_instances()
    instances_for_termination = []
    for instance in instances:
        if instance.get('Old') \
                or instance.get('NoKey') \
                or instance.get('NonWhitelistedInstanceType'):
            if instance.get('State', {}).get('Name') == 'running':
                instances_for_termination.append(instance)
    return instances_for_termination


def terminate_instances(instance_ids_to_terminate=()):
    if not instance_ids_to_terminate:
        instances = get_instances_for_termination()
        instance_ids_to_terminate = [i.get('InstanceId') for i in instances]

    ec2_client = boto_client('ec2')
    response = ec2_client.terminate_instances(InstanceIds=instance_ids_to_terminate)

    AWSCommandResponse.objects.create(
        command='terminate_instances',
        response=pformat(response, indent=4)
    )