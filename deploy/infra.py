import logging
from typing import TYPE_CHECKING

from deploy.config import (
    AWS_KEY_PAIR_NAME,
    AWS_RES_NAME,
    AWS_SECURITY_GROUP_NAME,
    DEV,
    IMAGE_ID,
    M4_L_NB,
    T2_L_NB,
)
from deploy.utils import ec2_res, elbv2_cli, get_default_vpc

if TYPE_CHECKING:
    from mypy_boto3_ec2.service_resource import (
        Instance,
        KeyPair,
        SecurityGroup,
        Vpc,
    )

logger = logging.getLogger(__name__)


def setup_infra():
    vpc = get_default_vpc()
    kp = _setup_key_pair()
    sg = _setup_security_group(vpc)
    instances = _launch_instances(sg, kp)
    _setup_load_balancer(sg, vpc)
    return instances


def _setup_key_pair():
    logger.info('Setting up key pair')
    key_pair = ec2_res.create_key_pair(KeyName=AWS_KEY_PAIR_NAME)

    with open(f'{AWS_KEY_PAIR_NAME}.pem', 'w') as f:
        f.write(key_pair.key_material)

    return key_pair


def _setup_security_group(vpc: 'Vpc'):
    logger.info('Setting up security group')
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


def _launch_instances(sg: 'SecurityGroup', kp: 'KeyPair') -> list['Instance']:
    logger.info('Launching instances')
    instances_m4 = ec2_res.create_instances(
        KeyName=kp.key_name,
        SecurityGroupIds=[sg.id],
        InstanceType='m4.large',
        ImageId=IMAGE_ID,
        MaxCount=M4_L_NB if not DEV else 1,
        MinCount=M4_L_NB if not DEV else 1,
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
        InstanceType='t2.large',
        ImageId=IMAGE_ID,
        MaxCount=T2_L_NB if not DEV else 1,
        MinCount=T2_L_NB if not DEV else 1,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': AWS_RES_NAME},
            ]
        }]
    )
    instances = instances_m4 + instances_t2

    for instance in instances:
        logger.info(f'Waiting for {instance=} to be ready')
        instance.wait_until_running()
        instance.reload()
        logger.debug(instance.public_ip_address)

    logger.info(instances)
    return instances


def _setup_load_balancer(sg: 'SecurityGroup', vpc: 'Vpc'):
    logger.info('Setting up load balancer')
    subnets = [subnet.id for subnet in vpc.subnets.all()]
    lb = elbv2_cli.create_load_balancer(
        Name=AWS_RES_NAME,
        Subnets=subnets,
        SecurityGroups=[sg.id],
    )
    logger.debug(lb)
