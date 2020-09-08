import boto3
import os
from datetime import datetime, timedelta

current_date_time = datetime.utcnow()

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
        for vol in volume_id[0:1]:
            date_strip = datetime.strptime(vol,'%H:%M:%S')
            get = (date_strip + timedelta(minutes=int(value)))
            additional_time = '{:%H:%M:%S}'.format(get)
            print('utc_now',now)
            print('additional',additional_time)
            if now > additional_time:
                print(0)
            else:
                print(1)

# Convert EPOCH to UTC
# datetime.datetime.utcfromtimestamp(1347517370).strftime('%Y-%m-%d %H:%M:%S')
#   '2012-09-13 06:22:50'

# Convert UTC to EPOCH
# import datetime
# timestamp = datetime.datetime(2017, 12, 1, 0, 0).timestamp()
# print(timestamp)