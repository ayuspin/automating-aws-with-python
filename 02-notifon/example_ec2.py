# coding: utf-8
get_ipython().run_line_magic('history', '')
import boto3 
session = boto3.Session(profile_name='pythonAutomation')
ec2 = session.resource('ec2')
ec2.instances.all()
list(ec2.instances.all())
inst = ec2.Instance(id='i-04765f0e38397bafb')
inst.public_dns_name
inst.security_groups
security_group_id = inst.security_groups[['GroupId']] 

security_group = ec2.SecurityGroup(security_group_id)
security_group_id = inst.security_groups[['GroupId']]
security_group_id = inst.security_groups[0]['GroupId']
security_group_id = inst.security_groups[['GroupId']] 

security_group = ec2.SecurityGroup(security_group_id)
security_group = ec2.SecurityGroup(security_group_id)
security_group.ip_permissions
security_group.revoke_ingress()
security_group.ip_permissions.remove()
security_group.ip_permissions.remove(all)
security_group.ip_permissions
security_group.revoke_ingress(CidrIp='84.207.230.30/32', FromPort=22)
security_group.revoke_ingress(CidrIp='84.207.230.30/32', FromPort=22, IpProtocol='tcp')
security_group.revoke_ingress(CidrIp='84.207.230.30/32', FromPort=22, IpProtocol='tcp', ToPort=22)
security_group.ip_permissions
security_group.authorize_ingress(IpPermissions=[{'FromPort': 22,'IpRanges': [{'CidrIp':'84.207.230.30/32'}],'ToPort': 22}])
security_group.authorize_ingress(IpPermissions=[{'FromPort': 22, 'IpProtocol': 'tcp', 'IpRanges': [{'CidrIp':'84.207.230.30/32'}],'ToPort': 22}])
security_group.ip_permissions
security_group.authorize_ingress(IpPermissions=[{'FromPort': 22, 'IpProtocol': 'tcp', 'IpRanges': [{'CidrIp':'0.0.0.0/0'}],'ToPort': 22}])
security_group.ip_permissions
security_group.authorize_ingress(IpPermissions=[{'FromPort': 80, 'IpProtocol': 'tcp', 'IpRanges': [{'CidrIp':'0.0.0.0/0'}],'ToPort': 80}])
security_group.ip_permissions
inst.public_dns_name
get_ipython().run_line_magic('history', '')
