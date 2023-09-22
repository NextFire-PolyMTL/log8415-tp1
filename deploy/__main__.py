from typing import TYPE_CHECKING

from deploy.config import AWS_RES_NAME, AWS_SECURITY_GROUP_NAME, IMAGE_ID, DEV
from deploy.utils import ec2_res, elbv2_cli, get_default_vpc, get_default_key_pair, SCRIPT

if TYPE_CHECKING:
    from mypy_boto3_ec2.service_resource import Vpc, SecurityGroup


def setup_security_groups(vpc: 'Vpc'):
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
                "IpRanges": [
                    {"CidrIp": "0.0.0.0/0", "Description": "internet"},
                ],
            },
        ],
    )
    return sg


def setup_instances(sg: 'SecurityGroup'):
    if DEV:
        instances = ec2_res.create_instances(
            KeyName=get_default_key_pair().key_name,
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
        for instance in instances:
            instance.wait_until_running()
            instance.reload()
            print(instance.public_ip_address)

        print(instances)
        return

    instances_m4 = ec2_res.create_instances(
        KeyName=get_default_key_pair().key_name,
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
    instances_T2 = ec2_res.create_instances(
    instances_t2 = ec2_res.create_instances(
        KeyName=get_default_key_pair().key_name,
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
    print(instances_m4, instances_t2)


def setup_load_balancer(vpc: 'Vpc'):
    subnets = [subnet.id for subnet in vpc.subnets.all()]
    lb = elbv2_cli.create_load_balancer(Name=AWS_RES_NAME, Subnets=subnets)
    print(lb)


def main():
    vpc = get_default_vpc()
    sg = setup_security_groups(vpc)
    setup_instances(sg)
    setup_load_balancer(vpc)


if __name__ == '__main__':
    main()
