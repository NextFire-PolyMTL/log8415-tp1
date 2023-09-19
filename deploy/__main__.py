from typing import TYPE_CHECKING

from deploy.config import AWS_RES_NAME, IMAGE_ID
from deploy.utils import ec2_res, elbv2_cli, get_default_vpc

if TYPE_CHECKING:
    from mypy_boto3_ec2.service_resource import Vpc


def setup_instances():
    instances_M4 = ec2_res.create_instances(
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
    instances_T2 = ec2_res.create_instances(
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
    print(instances_M4, instances_T2)


def setup_load_balancer(vpc: 'Vpc'):
    subnets = [subnet.id for subnet in vpc.subnets.all()]
    lb = elbv2_cli.create_load_balancer(Name=AWS_RES_NAME, Subnets=subnets)
    print(lb)


def main():
    vpc = get_default_vpc()
    setup_instances()
    setup_load_balancer(vpc)


if __name__ == '__main__':
    main()
