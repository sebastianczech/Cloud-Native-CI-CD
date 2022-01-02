import botocore
import pytest

# sys.path.append(os.path.abspath('../src'))
import app.src.main_boto3 as main_boto3
from app.src.main_boto3 import LocalstackConfig


def test_hostname_is_not_empty():
    # given

    # when
    hostname = main_boto3.info_hostname()

    # then
    assert len(hostname) > 0


def test_config_is_not_empty():
    # given

    # when
    config = main_boto3.info_config()

    # then
    assert config == 'None'


def test_time_is_not_empty():
    # given

    # when
    time = main_boto3.info_time()

    # then
    assert ":" in time


def test_cannot_get_s3_buckets_if_localstack_not_working():
    with pytest.raises(botocore.exceptions.EndpointConnectionError) as exception_info:
        localstack_config = LocalstackConfig(endpoint_url="http://localhost:9999",
                                             use_ssl=False,
                                             aws_access_key_id='test',
                                             aws_secret_access_key='test',
                                             region_name='us-east-1')
        s3 = list(main_boto3.s3_list_buckets(localstack_config))
    assert "Could not connect to the endpoint" in str(exception_info)


def test_bucket_is_created():
    # given

    # when
    main_boto3.s3_create_bucket(main_boto3.localstack_config(), "demo-bucket-py-test")
    buckets = [bucket["Name"] for bucket in main_boto3.s3_list_buckets(main_boto3.localstack_config())['Buckets']]
    # main_boto3.s3_upload_file(main_boto3.localstack_config(), "demo-bucket-py-test")

    # then
    assert "demo-bucket-py-test" in buckets
