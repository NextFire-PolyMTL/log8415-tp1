import logging

import boto3
from botocore.exceptions import ClientError
from paramiko import SSHClient

logger = logging.getLogger(__name__)

ec2_cli = boto3.client('ec2')
ec2_res = boto3.resource('ec2')
elbv2_cli = boto3.client('elbv2')


def get_default_vpc():
    vpcs_desc = ec2_cli.describe_vpcs(
        Filters=[{'Name': 'is-default', 'Values': ['true']}])
    try:
        default_vpc_id = vpcs_desc['Vpcs'][0]['VpcId']
    except Exception as e:
        raise RuntimeError('Default VPC not found') from e
    vpc = ec2_res.Vpc(default_vpc_id)
    logger.debug(vpc)
    return vpc


class SSHExecError(RuntimeError):
    pass


def ssh_exec(ssh_client: SSHClient, cmd: str):
    stdin, stdout, stderr = ssh_client.exec_command(cmd, get_pty=True)
    status = stdout.channel.recv_exit_status()
    logger.info('\n' + stdout.read().decode().strip())
    if status != 0:
        raise SSHExecError(stderr.read().decode())


def get_error_code(e: ClientError):
    error = e.response.get('Error', {})
    error_code = error.get('Code', 'Unknown')
    return error_code
