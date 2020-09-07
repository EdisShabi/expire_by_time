import boto3
import os
from datetime import datetime, timedelta

current_date_time = datetime.now()

ct = boto3.session.Session(profile_name='aws-im-dev')
cfn = ct.client('cloudformation',region_name='us-east-1')
ec2 = ct.resource('ec2', region_name = 'us-east-1')
stackname = []
instance_id = []
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
    for tag in response.tags:
        tags[tag['Key']] = tag['Value']

for key, value in tags.items():
    if key == 'CCC_EXPIRY_TIME':
        print(value)
        print('{:%H:%M:%S}'.format(current_date_time))
        print('{:%H:%M:%S}'.format(current_date_time.now() + timedelta(hours=int(value))))