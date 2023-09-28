import logging
from typing import TYPE_CHECKING

from deploy.bootstrap import bootstrap_instance
from deploy.config import (
    AWS_KEY_PAIR_NAME,
    AWS_RES_NAME,
    AWS_SECURITY_GROUP_NAME,
    DEV,
    IMAGE_ID,
    LOG_LEVEL,
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
        bootstrap_instance(inst, i)


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    main()
