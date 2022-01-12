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


# Examples of usage each below service is based on:
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html


def s3_list_buckets(s3):
    return s3.list_buckets()


def s3_create_bucket(s3, bucket):
    s3.create_bucket(Bucket=bucket)


def s3_upload_file(s3, bucket):
    binary_data = b'Binary data stored in S3'
    s3.put_object(Body=binary_data, Bucket=bucket, Key='simple_file_with_binary_data.txt')


def s3_list_object_in_bucket(s3, bucket):
    return s3.list_objects(Bucket=bucket)['Contents']


def sns_list_topics(sns):
    return sns.list_topics()


def sns_create_topic(sns, topic):
    sns.create_topic(Name=topic)


def sqs_list_queues(sqs):
    return sqs.list_queues()


def sqs_create_queue(sqs, queue):
    sqs.create_queue(QueueName=queue)


def dynamodb_delete_table(dynamodb, table_name):
    dynamodb.delete_table(
        TableName=table_name
    )


def dynamodb_create_table(dynamodb, table_name):
    dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'FirstName',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'LastName',
                'AttributeType': 'S'
            },
        ],
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'FirstName',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'LastName',
                'KeyType': 'RANGE'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 123,
            'WriteCapacityUnits': 123
        },
        Tags=[
            {
                'Key': 'Owner',
                'Value': 'Sebastian'
            },
        ]
    )


def dynamodb_list_tables(dynamodb):
    return dynamodb.list_tables()


if __name__ == "__main__":
    # Print host, config and time
    print("HOST: " + info_hostname())
    print("LOCALSTACK: " + localstack_url())
    print("CONFIG: " + info_config())
    print("TIME: ", info_time())

    # Create dynamodb table
    dynamodb_create_table(localstack_config_for_service('dynamodb', localstack_config()), 'demo-dynamodb-py')

    # Print out dynamodb tables names
    print("\nDynamoDB tables:")
    for table in dynamodb_list_tables(localstack_config_for_service('dynamodb', localstack_config()))['TableNames']:
        print("- " + table)

    # Delete dynamodb table
    dynamodb_delete_table(localstack_config_for_service('dynamodb', localstack_config()), 'demo-dynamodb-py')

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

    # Create SNS topic
    sns_create_topic(localstack_config_for_service('sns', localstack_config()), 'demo-sns-py')

    # Print out topics names
    print("\nSNS topics:")
    for topic in sns_list_topics(localstack_config_for_service('sns', localstack_config()))['Topics']:
        print("- " + topic['TopicArn'])

    # Create SQS queue
    sqs_create_queue(localstack_config_for_service('sqs', localstack_config()), 'demo-sqs-py')

    # Print out queues names
    print("\nSQS queues:")
    for queue in sqs_list_queues(localstack_config_for_service('sqs', localstack_config()))['QueueUrls']:
        print("- " + queue)

