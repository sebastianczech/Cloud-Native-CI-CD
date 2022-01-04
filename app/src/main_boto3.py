import datetime
import os
import socket

import boto3


class LocalstackConfig:
    def __init__(self, endpoint_url, use_ssl, aws_access_key_id, aws_secret_access_key, region_name):
        self.endpoint_url = endpoint_url
        self.use_ssl = use_ssl
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name


def info_hostname():
    return socket.gethostname()


def info_config():
    return str(os.environ.get('PYTHON_HOSTNAME_ENV_VERSION'))


def info_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def localstack_url():
    if 'LOCALSTACK_HOST' in os.environ:
        return "http://" + str(os.environ.get('LOCALSTACK_HOST')) + ":4566"
    else:
        return "http://localhost:4566"


def s3_list_buckets(s3):
    return s3.list_buckets()


def s3_upload_file(s3, bucket):
    binary_data = b'Binary data stored in S3'
    s3.put_object(Body=binary_data, Bucket=bucket, Key='simple_file_with_binary_data.txt')


def s3_create_bucket(s3, bucket):
    s3.create_bucket(Bucket=bucket)


def s3_list_object_in_bucket(s3, bucket):
    return s3.list_objects(Bucket=bucket)['Contents']


def sns_list_topics(sns):
    return sns.list_topics()


def localstack_config():
    return LocalstackConfig(endpoint_url=localstack_url(),
                            use_ssl=False,
                            aws_access_key_id='test',
                            aws_secret_access_key='test',
                            region_name='us-east-1')


def localstack_config_for_service(service, config):
    return boto3.client(service,
                        endpoint_url=config.endpoint_url,
                        use_ssl=config.use_ssl,
                        aws_access_key_id=config.aws_access_key_id,
                        aws_secret_access_key=config.aws_secret_access_key,
                        region_name=config.region_name)


if __name__ == "__main__":
    # Print host, config and time
    print("HOST: " + info_hostname())
    print("LOCALSTACK: " + localstack_url())
    print("CONFIG: " + info_config())
    print("TIME: ", info_time())

    # Create bucket if not exists
    s3_create_bucket(localstack_config_for_service('s3', localstack_config()), 'demo-bucket-py')

    # Upload binary data
    s3_upload_file(localstack_config_for_service('s3', localstack_config()), 'demo-bucket-py')

    # Print out bucket names
    print("\nS3 buckets:")
    for bucket in s3_list_buckets(localstack_config_for_service('s3', localstack_config()))['Buckets']:
        print("- " + bucket['Name'])

    # Print out bucket files
    print("\nFiles in demo-bucket-py:")
    for obj in s3_list_object_in_bucket(localstack_config_for_service('s3', localstack_config()), 'demo-bucket-py'):
        print("- " + obj['Key'])

    # Print out topics names
    print("\nSNS topic:")
    for topic in sns_list_topics(localstack_config_for_service('sns', localstack_config()))['Topics']:
        print("- " + topic['TopicArn'])
