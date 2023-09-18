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


def main():
    create_instances()
    pass


if __name__ == "__main__":
    ec2_res = boto3.resource('ec2')
    main()
