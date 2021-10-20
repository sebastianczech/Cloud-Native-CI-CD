import sys
import os
import pytest
import localstack_client.session as boto3
import botocore
sys.path.append(os.path.abspath('../src'))
import main_localstack_client


def test_hostname_is_not_empty():
    # given

    # when
    hostname = main_localstack_client.info_hostname()

    # then
    assert len(hostname) > 0


def test_config_is_not_empty():
    # given

    # when
    config = main_localstack_client.info_config()

    # then
    assert config == 'None'


def test_time_is_not_empty():
    # given

    # when
    time = main_localstack_client.info_time()

    # then
    assert ":" in time


# def test_cannot_get_s3_buckets_if_localstack_not_working():
#     with pytest.raises(botocore.exceptions.EndpointConnectionError) as exception_info:
#         s3 = list(main_localstack_client.s3_list_buckets())
#     assert "Could not connect to the endpoint" in str(exception_info)
