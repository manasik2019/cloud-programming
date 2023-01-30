import boto3
import logging
from botocore.exceptions import ClientError
import os
import time

#Then use the session to get the resource
s3 = boto3.resource('s3')


bucket_name = input("please enter the bucket name: ")

my_bucket = s3.Bucket(bucket_name)

#print bucket objects
print("the contents of " + bucket_name + " are: ")
for my_bucket_object in my_bucket.objects.all():
    print(my_bucket_object.key)