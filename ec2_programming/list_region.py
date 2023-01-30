import boto3

ec2 = boto3.client('ec2')

#Retrieves all regions/endpoints that work with EC2
response = ec2.describe_regions()

for r in response['Regions']:
    print("RegionName: " + r['RegionName'] + ", Endpoint: " + r['Endpoint'])

