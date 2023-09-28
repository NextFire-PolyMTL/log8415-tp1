import io
import logging
import tarfile
from typing import TYPE_CHECKING

import backoff
import requests
from paramiko import AutoAddPolicy, RSAKey, SSHClient, ssh_exception

from deploy.config import AWS_KEY_PAIR_NAME

if TYPE_CHECKING:
    from mypy_boto3_ec2.service_resource import Instance

logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.expo,
                      (ssh_exception.NoValidConnectionsError, TimeoutError),
                      max_time=300)
def bootstrap_instance(instance: 'Instance', i: int):
    logger.info(f"Bootstrapping instance #{i+1} {instance=}")
    ssh_key = RSAKey.from_private_key_file(f'{AWS_KEY_PAIR_NAME}.pem')
    with SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(
            hostname=instance.public_ip_address,
            username='ubuntu',
            pkey=ssh_key,
        )
        _setup_docker(ssh_client)
        _build_app(ssh_client)
        _run_app(ssh_client, i)
    _check_app(instance)


def _setup_docker(ssh_client: SSHClient):
    logger.info('Setting up docker')
    _ssh_exec(ssh_client,
              # force restart (and wait) snapd to be sure it is ready to use
              r'sudo systemctl restart snapd.seeded.service && '
              r'sudo snap install docker')


def _build_app(ssh_client: SSHClient):
    logger.info('Building app')
    with ssh_client.open_sftp() as sftp:
        with io.BytesIO() as f:
            with tarfile.open(fileobj=f, mode='w:gz') as tar:
                tar.add('pyproject.toml')
                tar.add('poetry.lock')
                tar.add('app/')
            f.seek(0)
            sftp.putfo(f, 'src.tar.gz')
    _ssh_exec(
        ssh_client, r"""
            mkdir -p src
            tar xzf src.tar.gz -C src/
            sudo docker build -t app -f src/app/Dockerfile src/
            """)


def _run_app(ssh_client: SSHClient, instance_number: int):
    logger.info('Running app')
    _ssh_exec(
        ssh_client,
        rf'sudo docker run -d -p 80:8000 -e INSTANCE_NUMBER={instance_number+1} app')


def _check_app(instance: 'Instance'):
    request_url = f'http://{instance.public_ip_address}'
    logger.info(f'Checking app at {request_url}')
    response = requests.get(request_url)
    response.raise_for_status()
    logger.info(response.text)


def _ssh_exec(ssh_client: SSHClient, cmd: str):
    stdin, stdout, stderr = ssh_client.exec_command(cmd, get_pty=True)
    status = stdout.channel.recv_exit_status()
    logger.debug(stdout.read().decode())
    if status != 0:
        raise RuntimeError('_ssh_exec failed', stderr.read().decode())
