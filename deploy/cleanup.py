import boto3


def main():
    # Terminate EC2 instances
    ec2_res = boto3.resource('ec2')
    instances = ec2_res.instances.all()
    for inst in instances:
        if inst.state['Name'] in ('pending', 'running'):
            print(f"Terminating instance: {inst}")
            inst.terminate()

    # Delete load balancers
    elbv2_cli = boto3.client('elbv2')
    lbs = elbv2_cli.describe_load_balancers()
    for lb in lbs['LoadBalancers']:
        arn = lb['LoadBalancerArn']
        print(f"Deleting load balancer: {arn}")
        elbv2_cli.delete_load_balancer(LoadBalancerArn=arn)


if __name__ == '__main__':
    main()
