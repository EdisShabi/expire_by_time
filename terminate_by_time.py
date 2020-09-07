import boto3
import os
from datetime import datetime, timedelta

current_date_time = datetime.now()

ct = boto3.session.Session(profile_name='aws-im-dev')
cfn = ct.client('cloudformation',region_name='us-east-1')
ec2 = ct.resource('ec2', region_name = 'us-east-1')
stackname = []
instance_id = []
volume_id = []
tags = {}
for stack in cfn.list_stacks()['StackSummaries']:
    stackname.append(stack['StackName'])
for stackX in stackname:
    try:
        response = cfn.describe_stack_resources(StackName=stackX)
        for resource in response['StackResources']:
                if resource['ResourceType'] == 'AWS::EC2::Instance':
                    instance_id.append(resource['PhysicalResourceId'])
    except:
        pass
for instance in instance_id:
    response = ec2.Instance(instance)
    volume = response.volumes.all()
    for v in volume:
        volume_id.append(v.create_time.strftime("%H:%M:%S"))
    for tag in response.tags:
        tags[tag['Key']] = tag['Value']

for key, value in tags.items():
    if key == 'CCC_EXPIRY_TIME':
        now = ('{:%H:%M:%S}'.format(current_date_time))
        print(value)
        for vol in volume_id[0:1]:
            date_strip = datetime.strptime(vol,'%H:%M:%S')
            print(vol)
            get = (date_strip + timedelta(hours=int(value)))
            additional_time = '{:%H:%M:%S}'.format(get)
            print('{:%H:%M:%S}'.format(get))
            if current_date_time > get:
                print(0)
            else:
                print(1)
