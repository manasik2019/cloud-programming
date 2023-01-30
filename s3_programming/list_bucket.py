
import boto3

#to get the region choice from user
region_choice = input("please enter the region of your choice: ")

#create s3 client
s3_client = boto3.client('s3', region_name=region_choice)

#list all buckets
all_buckets = s3_client.list_buckets()

#test the bucket region with the entered region to print it out
for bucket in all_buckets['Buckets']:
    bucket_region = s3_client.get_bucket_location(Bucket=bucket["Name"])["LocationConstraint"]

    if bucket_region == region_choice:
        print(bucket["Name"])
    else: 
        continue