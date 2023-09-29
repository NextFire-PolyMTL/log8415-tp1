import io
import logging
import tarfile
from typing import TYPE_CHECKING

import backoff
import requests
from paramiko import AutoAddPolicy, RSAKey, SSHClient, ssh_exception

from deploy.config import AWS_KEY_PAIR_NAME, SSH_USERNAME
from deploy.utils import SSHExecError, ssh_exec

if TYPE_CHECKING:
    from mypy_boto3_ec2.service_resource import Instance

logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.constant,
                      (ssh_exception.NoValidConnectionsError, TimeoutError))
def bootstrap_instance(instance: 'Instance', instance_number: int):
    logger.info(f"Bootstrapping instance #{instance_number+1} {instance=}")
    ssh_key = RSAKey.from_private_key_file(f'{AWS_KEY_PAIR_NAME}.pem')
    with SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(
            hostname=instance.public_ip_address,
            username=SSH_USERNAME,
            pkey=ssh_key,
        )
        _setup_docker(ssh_client)
        _push_sources(ssh_client)
        _build_app(ssh_client)
        _start_app(ssh_client, instance_number)
    _check_app(instance)


@backoff.on_exception(backoff.constant, SSHExecError)
def _setup_docker(ssh_client: SSHClient):
    logger.info('Setting up docker')
    ssh_exec(ssh_client, r'sudo snap install docker')


def _push_sources(ssh_client: SSHClient):
    logger.info('Pushing sources')
    with ssh_client.open_sftp() as sftp:
        with io.BytesIO() as f:
            with tarfile.open(fileobj=f, mode='w:gz') as tar:
                tar.add('pyproject.toml')
                tar.add('poetry.lock')
                tar.add('app/')
            f.seek(0)
            sftp.putfo(f, 'src.tar.gz')


@backoff.on_exception(backoff.constant, SSHExecError)
def _build_app(ssh_client: SSHClient):
    logger.info('Building app')
    ssh_exec(
        ssh_client, r"""
            rm -rf src && mkdir -p src
            tar xzf src.tar.gz -C src/
            sudo docker build -t app -f src/app/Dockerfile src/
            """)


@backoff.on_exception(backoff.constant, SSHExecError)
def _start_app(ssh_client: SSHClient, instance_number: int):
    logger.info('Start app')
    ssh_exec(
        ssh_client,
        rf"""
        sudo docker rm -f app
        sudo docker run --name app -d -p 80:8000 \
            -e INSTANCE_NUMBER={instance_number+1} app
        """)


@backoff.on_exception(backoff.constant, (requests.HTTPError, requests.ConnectionError))
def _check_app(instance: 'Instance'):
    request_url = f'http://{instance.public_ip_address}'
    logger.info(f'Checking app at {request_url}')
    response = requests.get(request_url)
    response.raise_for_status()
    logger.info(response.text)
