import requests
import os
import boto3

def localstack_url(path):
    protocol = os.environ.get('INFRA_LOCALSTACK_PROTOCOL') if os.environ.get('INFRA_LOCALSTACK_PROTOCOL') is not None else 'http'
    address = os.environ.get('INFRA_LOCALSTACK_ADDRESS') if os.environ.get('INFRA_LOCALSTACK_ADDRESS') is not None else '127.0.0.1'
    port = os.environ.get('INFRA_LOCALSTACK_PORT') if os.environ.get('INFRA_LOCALSTACK_PORT') is not None else '4566'
    return protocol + '://' + address + ':' + port + '/' + path


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
    assert response.json()['services']['s3'] == 'running'


def test_localstack_bucket_can_be_created():
    # given
    s3 = boto3.client('s3',
                      endpoint_url=localstack_url(''),
                      use_ssl=False,
                      aws_access_key_id='test',
                      aws_secret_access_key='test',
                      region_name='us-east-1')
    bucket_name = 'demo-bucket-py-test'

    # when
    response_create_bucket = s3.create_bucket(Bucket=bucket_name)
    response_list_buckets = s3.list_buckets()
    buckets_names = [bucket['Name'] for bucket in response_list_buckets['Buckets']]

    # then
    assert response_create_bucket['ResponseMetadata']['HTTPStatusCode'] == 200
    assert response_list_buckets['ResponseMetadata']['HTTPStatusCode'] == 200
    assert bucket_name in buckets_names
