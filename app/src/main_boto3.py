import datetime
import os
import socket

import boto3


def info_hostname():
    return socket.gethostname()


def info_config():
    return str(os.environ.get('PYTHON_HOSTNAME_ENV_VERSION'))


def info_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def s3_list_buckets(endpoint_url, use_ssl, aws_access_key_id, aws_secret_access_key, region_name):
    s3 = boto3.client('s3',
                      endpoint_url=endpoint_url,
                      use_ssl=use_ssl,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=region_name)
    return s3.list_buckets()


if __name__ == "__main__":
    # Print host, config and time
    print("HOST: " + info_hostname())
    print("CONFIG: " + info_config())
    print("TIME: ", info_time())

    # Print out bucket names
    print("\nS3 buckets:")
    for bucket in s3_list_buckets(endpoint_url="http://localhost:4566",
                                  use_ssl=False,
                                  aws_access_key_id='test',
                                  aws_secret_access_key='test',
                                  region_name='us-east-1')['Buckets']:
        print("- " + bucket['Name'])
