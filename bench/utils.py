import logging
import re

import boto3

logger = logging.getLogger(__name__)

elbv2_cli = boto3.client('elbv2')
cw_cli = boto3.client('cloudwatch')

SPECIFIER_RE = re.compile(r'[^:\/]+\/[^\/]+\/[a-z0-9]+$')


def wait_lb(name: str):
    waiter = elbv2_cli.get_waiter('load_balancer_available')
    waiter.wait(Names=[name])


def get_lb_arn_dns(name: str):
    lbs = elbv2_cli.describe_load_balancers(Names=[name])
    if len(lbs['LoadBalancers']) == 0:
        raise RuntimeError(f"Load balancer {name} not found")
    lb = lbs['LoadBalancers'][0]
    lb_arn = lb.get('LoadBalancerArn')
    if lb_arn is None:
        raise RuntimeError('Load balancer ARN not found')
    lb_dns = lb.get('DNSName')
    if lb_dns is None:
        raise RuntimeError('Load balancer DNS name not found')
    return lb_arn, lb_dns


def get_tg_arn(name: str):
    tgs = elbv2_cli.describe_target_groups(Names=[name])
    if len(tgs['TargetGroups']) == 0:
        raise RuntimeError(f"Target group {name} not found")
    tg = tgs['TargetGroups'][0]
    tg_arn = tg.get('TargetGroupArn')
    if tg_arn is None:
        raise RuntimeError('Target group ARN not found')
    return tg_arn


def specifier_from_arn(arn: str):
    search = SPECIFIER_RE.search(arn)
    if search is None:
        raise RuntimeError(f"Could not match specifier regex in {arn}")
    return search.group()
