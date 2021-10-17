import boto3

import socket
import os
import datetime


def info_hostname():
    return socket.gethostname()


def info_config():
    return str(os.environ.get('PYTHON_HOSTNAME_ENV_VERSION'))


def info_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def s3_list_buckets():
    s3 = boto3.client('s3',
                      endpoint_url="http://localhost:4566",
                      use_ssl=False,
                      aws_access_key_id='test',
                      aws_secret_access_key='test',
                      region_name='us-east-1')
    return s3.list_buckets()


if __name__ == "__main__":
    # Print host, config and time
    print("HOST: " + info_hostname())
    print("CONFIG: " + info_config())
    print("TIME: ", info_time())

    # Print out bucket names
    print("\nS3 buckets:")
    for bucket in s3_list_buckets()['Buckets']:
        print("- " + bucket['Name'])
