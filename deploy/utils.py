import boto3

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
    print(vpc)
    return vpc


# Source: https://snapcraft.io/docker
SCRIPT = r"""
#!/bin/bash
sudo snap install docker

sudo addgroup --system docker
sudo adduser $USER docker
newgrp docker
sudo snap disable docker
sudo snap enable docker
"""
