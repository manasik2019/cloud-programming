import boto3
import logging
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region=None):
  
    # Create bucket
    try:
        if region is None:
            #bucket will be created in the default region (us-east-1)
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

region_choice = input("please enter the region of your choice: ")
bucket_name = input("please enter the bucket name: ")

print("bucket is being created ..... ")

create_bucket(bucket_name, region_choice)

print("new bucket has been created ... ")

# #three regions to create buckets in
# regions = ['eu-north-1', 'ca-central-1','eu-west-3']

# #three buckets names to be created in different regions
# bucket_names = ['manasik-lab2bucket', 'manasik-lab2bucket1', 'manasik-lab2bucket2']

# #creating three buckets in 3 different regions
# for i in regions:
#     print(i)
#     create_bucket(bucket_names[regions.index(i)], i)


