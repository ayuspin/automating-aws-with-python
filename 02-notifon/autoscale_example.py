# coding: utf-8
import boto3 
session = boto3.Session(profile_name='pythonAutomation')
as_client = boto3.client('autoscaling')
as_client = session.client('autoscaling')
as_client.describe_auto_scaling_groups
print(as_client.describe_auto_scaling_groups)
print(as_client.describe_auto_scaling_groups())
print(as_client.describe_auto_scaling_groups()['AutoScalingGroups'][0])
print(as_client.describe_auto_scaling_groups()['AutoScalingGroups'][0]['AutoScalingGroupName'])
as_client.describe_policies()
as_client.execute_policy(AutoScalingGroupName='NotifonGR', PolicyName='ScaleDown')
as_client.execute_policy(AutoScalingGroupName='NotifonGR', PolicyName='ScaleDown')
as_client.execute_policy(AutoScalingGroupName='NotifonGR', PolicyName='ScaleDown')
as_client.execute_policy(AutoScalingGroupName='NotifonGR', PolicyName='ScaleUP')
