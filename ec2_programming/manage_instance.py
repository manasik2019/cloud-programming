import boto3
from botocore.exceptions import ClientError
import datetime

#create ec2 client
ec2 = boto3.client('ec2')
ec = boto3.resource('ec2')


#create a key pair
ec2 = boto3.client('ec2')
response = ec2.create_key_pair(KeyName='lab3_key_pair')


#list the created key pair
print('Please provide key_pair name for details: ')
name = input()
key_pair = ec2.describe_key_pairs(KeyNames=[name])

print('Key pair details .. ')
print('Key pair ID: ' + key_pair['KeyPairs'][0]['KeyPairId'])
print('key pair type: '+ key_pair['KeyPairs'][0]['KeyType'])
print('Key Fingerprint: ' + key_pair['KeyPairs'][0]['KeyFingerprint'])

print('\n')

#create a security group
response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

try:
    response = ec2.create_security_group(GroupName='lab3_security_group',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress Successfully Set %s' % data)
except ClientError as e:
    print(e)

#list the security group
security_group = ec2.describe_security_groups(GroupNames=['lab3_security_group'])
print('The following security group created ... ')
print(security_group)
print('\n')

#create instance
instance = ec.create_instances(
    ImageId='ami-0efda064d1b5e46a5',
    InstanceType='t3.micro',
    KeyName='lab3_key_pair',
    MaxCount=2,
    MinCount=2,
    SecurityGroupIds=['sg-06a7fe9c3aa769f87'], 
    InstanceInitiatedShutdownBehavior='stop'
    )

#retreive the details of the instances
instance_details = ec2.describe_instances(
    InstanceIds=[
        'i-0eb0378fa1e6fe0fd',
        'i-079f59dfcd157d852'
    ]
)

for r in instance_details['Reservations'][0]['Instances']:

    print('Deatils for Instance with ID %s .... ' %(r['InstanceId']))
    print('Availability zone: ' + r['Placement']['AvailabilityZone'])
    print('Image ID: ' + r['ImageId'])
    print('Instance Type: '+ r['InstanceType'])
    print('Key Pair Name: ' + r['KeyName'])
    print('Private DNS Name: '+r['PrivateDnsName'])
    print('Public DNS Name: ' + r['PublicDnsName'])
    print('\n')
    


#retreive the status of the running instances
# instance_status = ec2.describe_instance_status(
#     InstanceIds=[
#         'i-0eb0378fa1e6fe0fd'
#     ]
# )

# print('Instance i-0eb0378fa1e6fe0fd State: ' + instance_status['InstanceStatuses'][0]['InstanceState']['Name'])
# print('Instance i-0eb0378fa1e6fe0fd Staus: ' + instance_status['InstanceStatuses'][0]['InstanceStatus']['Details'][0]['Status'])


# print('Staus of the created instances ... ')
# for r in instance_status['InstanceStatuses']: 
#     print(r)


#stop intances
stop_instance = ec2.stop_instances(
    InstanceIds=[
        'i-0eb0378fa1e6fe0fd',
        'i-079f59dfcd157d852'
    ])

print('Staus of ec2 instances .... ')
for r in stop_instance['StoppingInstances']:
    print('Instance %s current state is: %s , previous state is: %s' %(r['InstanceId'], r['CurrentState']['Name'], r['PreviousState']['Name']))


