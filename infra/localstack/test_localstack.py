import requests
import os
import boto3


def localstack_url(path):
    protocol = os.environ.get('INFRA_LOCALSTACK_PROTOCOL') if os.environ.get('INFRA_LOCALSTACK_PROTOCOL') is not None else 'http'
    address = os.environ.get('INFRA_LOCALSTACK_ADDRESS') if os.environ.get('INFRA_LOCALSTACK_ADDRESS') is not None else '127.0.0.1'
    port = os.environ.get('INFRA_LOCALSTACK_PORT') if os.environ.get('INFRA_LOCALSTACK_PORT') is not None else '4566'
    return protocol + '://' + address + ':' + port + '/' + path


def localstack_config(service_name):
    return boto3.client(service_name,
                      endpoint_url=localstack_url(''),
                      use_ssl=False,
                      aws_access_key_id='test',
                      aws_secret_access_key='test',
                      region_name='us-east-1')


def test_localstack_in_docker_is_running():
    # given

    # when
    response = requests.get(localstack_url('health'))

    # then
    assert response.status_code == 200


def test_localstack_s3_service_is_running():
    # given

    # when
    response = requests.get(localstack_url('health'))
    print(response.json())

    # then
    assert response.status_code == 200
    assert response.json()['services']['s3'] == 'running' or response.json()['services']['s3'] == 'available'


def test_localstack_s3_bucket_can_be_created():
    # given
    s3 = localstack_config('s3')
    bucket_name = 'demo-bucket-py-test'

    # when
    response_create_bucket = s3.create_bucket(Bucket=bucket_name)
    response_list_buckets = s3.list_buckets()
    buckets_names = [bucket['Name'] for bucket in response_list_buckets['Buckets']]

    # then
    assert response_create_bucket['ResponseMetadata']['HTTPStatusCode'] == 200
    assert response_list_buckets['ResponseMetadata']['HTTPStatusCode'] == 200
    assert bucket_name in buckets_names


def test_localstack_s3_file_is_uploaded_into_bucket():
    # given
    s3 = localstack_config('s3')
    bucket_name = 'demo-bucket-py-test'
    binary_data = b'Binary data stored in S3'
    file_name = 'test_file_with_binary_data.txt'

    # when
    response_create_bucket = s3.create_bucket(Bucket=bucket_name)
    response_upload_file = s3.put_object(Body=binary_data, Bucket=bucket_name, Key=file_name)
    response_files_in_buckets = s3.list_objects(Bucket=bucket_name)
    files_in_bucket = [file_in_bucket["Key"] for file_in_bucket in response_files_in_buckets['Contents']]

    # then
    assert response_create_bucket['ResponseMetadata']['HTTPStatusCode'] == 200
    assert response_upload_file['ResponseMetadata']['HTTPStatusCode'] == 200
    assert response_files_in_buckets['ResponseMetadata']['HTTPStatusCode'] == 200
    assert file_name in files_in_bucket


def test_localstack_sqs_service_is_running():
    # given

    # when
    response = requests.get(localstack_url('health'))
    print(response.json())

    # then
    assert response.status_code == 200
    assert response.json()['services']['sqs'] == 'running' or response.json()['services']['sqs'] == 'available'


def test_localstack_sqs_queue_can_be_created():
    # given
    sqs = localstack_config('sqs')
    queue_name = 'demo-sqs-py-test'

    # when
    response_create_queue = sqs.create_queue(QueueName=queue_name)
    response_list_queues = sqs.list_queues()
    queues_names = [queue.split("/")[-1] for queue in response_list_queues['QueueUrls']]

    # then
    assert response_create_queue['ResponseMetadata']['HTTPStatusCode'] == 200
    assert response_list_queues['ResponseMetadata']['HTTPStatusCode'] == 200
    assert queue_name in queues_names


def test_localstack_sns_service_is_running():
    # given

    # when
    response = requests.get(localstack_url('health'))
    print(response.json())

    # then
    assert response.status_code == 200
    assert response.json()['services']['sns'] == 'running' or response.json()['services']['sns'] == 'available'


def test_localstack_sns_topic_can_be_created():
    # given
    sns = localstack_config('sns')
    topic_name = 'demo-sns-py-test'

    # when
    response_create_topic = sns.create_topic(Name=topic_name)
    response_list_topic = sns.list_topics()
    topics_names = [queue["TopicArn"].split(":")[-1] for queue in response_list_topic['Topics']]

    # then
    assert response_create_topic['ResponseMetadata']['HTTPStatusCode'] == 200
    assert response_list_topic['ResponseMetadata']['HTTPStatusCode'] == 200
    assert topic_name in topics_names