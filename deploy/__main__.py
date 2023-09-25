import io
import logging
import tarfile
from typing import TYPE_CHECKING

from paramiko import AutoAddPolicy, RSAKey, SSHClient

from deploy.config import (
    AWS_KEY_PAIR_NAME,
    AWS_RES_NAME,
    AWS_SECURITY_GROUP_NAME,
    DEV,
    IMAGE_ID,
    LOG_LEVEL,
)
from deploy.utils import SCRIPT, ec2_res, elbv2_cli, get_default_vpc

if TYPE_CHECKING:
    from mypy_boto3_ec2.service_resource import (
        Instance,
        KeyPair,
        SecurityGroup,
        Vpc,
    )

logger = logging.getLogger(__name__)


def setup_key_pair():
    key_pair = ec2_res.create_key_pair(KeyName=AWS_KEY_PAIR_NAME)

    with open(f'{AWS_KEY_PAIR_NAME}.pem', 'w') as f:
        f.write(key_pair.key_material)

    return key_pair


def setup_security_group(vpc: 'Vpc'):
    sg = ec2_res.create_security_group(
        GroupName=AWS_SECURITY_GROUP_NAME,
        Description=AWS_SECURITY_GROUP_NAME,
        VpcId=vpc.id,
    )
    sg.authorize_ingress(
        IpPermissions=[
            {
                "FromPort": 22,
                "ToPort": 22,
                "IpProtocol": "tcp",
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
            {
                "FromPort": 80,
                "ToPort": 80,
                "IpProtocol": "tcp",
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
        ],
    )
    return sg


def setup_instances(sg: 'SecurityGroup', kp: 'KeyPair') -> list['Instance']:
    if DEV:
        instances = ec2_res.create_instances(
            KeyName=kp.key_name,
            SecurityGroupIds=[sg.id],
            UserData=SCRIPT,
            InstanceType='t2.micro',
            ImageId=IMAGE_ID,
            MaxCount=1,
            MinCount=1,
            Monitoring={'Enabled': True},
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': AWS_RES_NAME},
                ]
            }],
        )
    else:
        instances_m4 = ec2_res.create_instances(
            KeyName=kp.key_name,
            SecurityGroupIds=[sg.id],
            UserData=SCRIPT,
            InstanceType='m4.large',
            ImageId=IMAGE_ID,
            MaxCount=5,
            MinCount=5,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': AWS_RES_NAME},
                ]
            }]
        )
        instances_t2 = ec2_res.create_instances(
            KeyName=kp.key_name,
            SecurityGroupIds=[sg.id],
            UserData=SCRIPT,
            InstanceType='t2.large',
            ImageId=IMAGE_ID,
            MaxCount=5,
            MinCount=5,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': AWS_RES_NAME},
                ]
            }]
        )
        instances = instances_m4 + instances_t2

    for instance in instances:
        instance.wait_until_running()
        instance.reload()
        logger.info(instance.public_ip_address)

    logger.info(instances)
    return instances


def setup_load_balancer(sg: 'SecurityGroup', vpc: 'Vpc'):
    subnets = [subnet.id for subnet in vpc.subnets.all()]
    lb = elbv2_cli.create_load_balancer(
        Name=AWS_RES_NAME,
        Subnets=subnets,
        SecurityGroups=[sg.id],
    )
    logger.info(lb)


def upload_flask_app(instance: 'Instance', i: int):
    ssh_key = RSAKey.from_private_key_file(f'{AWS_KEY_PAIR_NAME}.pem')

    with SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(
            hostname=instance.public_ip_address,
            username='ubuntu',
            pkey=ssh_key,
        )

        with ssh_client.open_sftp() as sftp:
            with io.BytesIO() as f:
                with tarfile.open(fileobj=f, mode='w:gz') as tar:
                    tar.add('pyproject.toml')
                    tar.add('poetry.lock')
                    tar.add('app/')
                f.seek(0)
                sftp.putfo(f, 'src.tar.gz')

        logger.info('Building docker image...')
        exec_and_wait(
            ssh_client, r"""
            mkdir -p src
            tar xzf src.tar.gz -C src/
            cd src/
            sudo docker build -t app -f app/Dockerfile .
            """)

        logger.info('Running docker container...')
        exec_and_wait(
            ssh_client, f'sudo docker run -d -p 80:8000 -e INSTANCE_NUMBER={i+1} app')


def exec_and_wait(ssh_client: 'SSHClient', cmd: str):
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    status = stdout.channel.recv_exit_status()
    if status != 0:
        logger.error('An error occurred')
        for line in stderr.readlines():
            logger.error(line)
        ssh_client.close()
        raise RuntimeError('An error occurred')


def main():
    vpc = get_default_vpc()
    kp = setup_key_pair()
    sg = setup_security_group(vpc)
    instances = setup_instances(sg, kp)
    setup_load_balancer(sg, vpc)

    # Use this to use existing instance instead of creating new ones
    # instances = ec2_res.instances.filter(
    #     Filters=[
    #         {'Name': 'tag:Name', 'Values': [AWS_RES_NAME]},
    #         {'Name': 'instance-state-name', 'Values': ['pending', 'running']},
    #     ]
    # )

    for i, inst in enumerate(instances):
        upload_flask_app(inst, i)


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    main()
