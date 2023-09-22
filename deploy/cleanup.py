from deploy.config import AWS_RES_NAME, AWS_SECURITY_GROUP_NAME
from deploy.utils import ec2_res, elbv2_cli


def terminate_ec2():
    instances = ec2_res.instances.filter(
        Filters=[
            {'Name': 'tag:Name', 'Values': [AWS_RES_NAME]},
            {'Name': 'instance-state-name', 'Values': ['pending', 'running']},
        ]
    )
    for inst in instances:
        print(f"Terminating instance: {inst}")
        inst.terminate()


def delete_lb():
    lbs = elbv2_cli.describe_load_balancers()
    for lb in lbs['LoadBalancers']:
        name = lb.get('LoadBalancerName')
        if name == AWS_RES_NAME:
            arn = lb.get('LoadBalancerArn')
            if arn is None:
                raise RuntimeError('Load balancer ARN not found')
            print(f"Deleting load balancer: {arn}")
            elbv2_cli.delete_load_balancer(LoadBalancerArn=arn)
            break
    else:
        print('Load balancer not found')


def delete_security_groups():
    sg = ec2_res.SecurityGroup(AWS_SECURITY_GROUP_NAME)
    print(f"Deleting security group: {sg}")
    sg.delete()


def main():
    terminate_ec2()
    delete_lb()
    delete_security_groups()


if __name__ == '__main__':
    main()
