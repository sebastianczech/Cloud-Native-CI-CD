import localstack_client.session as boto3
import localstack_client

import socket
import os
import datetime


def info_hostname():
    return socket.gethostname()


def info_config():
    return str(os.environ.get('PYTHON_HOSTNAME_ENV_VERSION'))


def info_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def localstack_services():
    print("\nLOCALSTACK SERVICES:")
    for service in boto3.config.get_service_endpoints():
        print(service + " ---> " + boto3.config.get_service_endpoints()[service])


def s3_list_buckets():
    ### attempt # 1
    # os.environ['EDGE_PORT'] = "9999"
    # s3 = session.resource('s3')

    ### attetmpt # 2
    # os.environ["LOCALSTACK_HOST"] = host
    # session = localstack_client.session.Session()
    # s3 = session.resource('s3')

    ### attempt # 3
    # kwargs = {"localstack_host:: host}
    # session = localstack_client.session.Session(**kwargs)
    # s3 = session.resource('s3')

    s3 = boto3.resource('s3')
    return s3.buckets.all()


if __name__ == "__main__":
    # Print host, config and time
    print("HOST: " + info_hostname())
    print("CONFIG: " + info_config())
    print("TIME: ", info_time())

    # Print Localstack services
    localstack_services()

    # Print out bucket names
    print("\nS3 buckets:")
    for bucket in s3_list_buckets():
        print("- " + bucket.name)
