import boto3
import logging
from botocore.exceptions import ClientError
import os
import time


s3 = boto3.resource('s3')

bucket_name = input("please enter the bucket name: ")

my_bucket = s3.Bucket(bucket_name)

objects = []

#get the keys for objects in specific bucket
for my_bucket_object in my_bucket.objects.all():
    objects.append(my_bucket_object.key)

#delete objects
for i in objects:

    s3.Object(bucket_name, i).delete()

print("all " + bucket_name + " content have been deleted ")