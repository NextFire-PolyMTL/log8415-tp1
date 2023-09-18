import boto3


def create_instances():
    instances_M4 = ec2_res.create_instances(
        InstanceType="m4.large",
        ImageId="ami-053b0d53c279acc90", # ubuntu 22.04
        MaxCount=5,
        MinCount=5,
    )
    print(f"{instances_M4=}")

    instances_T2 = ec2_res.create_instances(
        InstanceType="t2.large",
        ImageId="ami-053b0d53c279acc90", # ubuntu 22.04
        MaxCount=5,
        MinCount=5,
    )
    print(f"{instances_T2=}")



def create_load_balancer():
    ec2_res.create_subnet(
        VpcId="",
        AvailabilityZone="us-east-1a",
    )

    ec2_res.create_subnet(
        VpcId="",
        AvailabilityZone="us-east-1b",
    )

    lbs = elbv2_cli.create_load_balancer(
        Name="LoadBalancerMain",
        # Subnets=["subnet-07486aa1dafa304a6", "subnet-025483a1116699746"]
        AvailabilityZones=["us-east-1a", "us-east-1b"] # type: ignore
    )
    print(f"{lbs=}")


def main():
    create_instances()
    create_load_balancer()
    pass


if __name__ == "__main__":
    ec2_res = boto3.resource('ec2')
    elbv2_cli = boto3.client('elbv2')
    main()
