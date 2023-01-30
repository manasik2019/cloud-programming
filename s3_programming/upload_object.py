import boto3
import logging
from botocore.exceptions import ClientError
import os
import time

def upload_file(file_name, bucket, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(bucket_name, object_name, file_name):
    #download file
    s3 = boto3.client('s3')
    try: 
        s3.download_file(bucket_name, object_name, file_name)
    
    except ClientError as e:
        logging.error(e)
        return False
    return True


bucket_names = ['manasik-lab2bucket', 'manasik-lab2bucket1', 'manasik-lab2bucket2']
files = ['1MB.zip', '10MB.bin', '100MB.bin', '500MB.bin']

bucket_name = input("please enter the bucket name: ")


#get the locations of buckets
for i in bucket_names:
    print(i)
    bucket_region = boto3.client('s3').get_bucket_location(Bucket=i)["LocationConstraint"]

#Upload files and test the latency
for j in files:
    start_time = time.time()
    print("uploading "+ j + " to "+ bucket_name + "....")
    upload_file(j, bucket_name)
    upload_file(j, i)
    print('time for uploading ' + j + ' to ' + i + ' in region ' + bucket_region +' is: ' + "--- %s seconds ---" % (time.time() - start_time))

print(" all objects have been uploaded")

#Download files and test the latency
for i in bucket_names:
    print(i)
    bucket_region = boto3.client('s3').get_bucket_location(Bucket=i)["LocationConstraint"]

    for j in files:
        start_time = time.time()
        download_file(i, j, j)
        print('time for downloading ' + j + ' from ' + i + ' in region ' + bucket_region +' is: ' + "--- %s seconds ---" % (time.time() - start_time))

