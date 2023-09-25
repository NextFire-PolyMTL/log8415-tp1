import logging

from deploy.config import (
    AWS_KEY_PAIR_NAME,
    AWS_RES_NAME,
    AWS_SECURITY_GROUP_NAME,
    LOG_LEVEL,
)
from deploy.utils import ec2_res, elbv2_cli

logger = logging.getLogger(__name__)


def terminate_ec2():
    instances = ec2_res.instances.filter(
        Filters=[
            {'Name': 'tag:Name', 'Values': [AWS_RES_NAME]},
            {'Name': 'instance-state-name', 'Values': ['pending', 'running']},
        ]
    )
    for inst in instances:
        logger.info(f"Terminating instance: {inst}")
        inst.terminate()
        inst.wait_until_terminated()


def delete_lb():
    lbs = elbv2_cli.describe_load_balancers()
    for lb in lbs['LoadBalancers']:
        name = lb.get('LoadBalancerName')
        if name == AWS_RES_NAME:
            arn = lb.get('LoadBalancerArn')
            if arn is None:
                raise RuntimeError('Load balancer ARN not found')
            logger.info(f"Deleting load balancer: {arn}")
            elbv2_cli.delete_load_balancer(LoadBalancerArn=arn)
            break
    else:
        logger.error('Load balancer not found')


def delete_key_pair():
    try:
        key_pairs = ec2_res.key_pairs.filter(
            KeyNames=[AWS_KEY_PAIR_NAME],
        )
        logger.info(f"Deleting key pair: {key_pairs}")
        for kp in key_pairs:
            kp.delete()
    except Exception as e:
        logger.exception(e)


def delete_security_groups():
    try:
        security_groups = ec2_res.security_groups.filter(
            GroupNames=[AWS_SECURITY_GROUP_NAME],
        )
        logger.info(f"Deleting security group: {security_groups}")
        for sg in security_groups:
            sg.delete()
    except Exception as e:
        logger.exception(e)


def main():
    terminate_ec2()
    delete_key_pair()
    delete_lb()
    delete_security_groups()


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    main()
