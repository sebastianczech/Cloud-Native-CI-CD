import requests
import os


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
