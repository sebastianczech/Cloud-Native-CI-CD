# import boto3
import localstack_client.session as boto3

import socket
import os
import datetime

# Print host, config and time
print("HOST: " + socket.gethostname())
print("CONFIG: " + str(os.environ.get('PYTHON_HOSTNAME_ENV_VERSION')))
print("TIME: ", datetime.datetime.now().strftime("%H:%M:%S"))

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
print("\nS3 buckets:")
for bucket in s3.buckets.all():
    print("- " + bucket.name)