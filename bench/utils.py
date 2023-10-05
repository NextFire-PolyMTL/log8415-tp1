import logging
import re

import boto3

from bench.config import LB_NAME

logger = logging.getLogger(__name__)

elbv2_cli = boto3.client('elbv2')
cw_cli = boto3.client('cloudwatch')

SPECIFIER_RE = re.compile(r'app/[A-Za-z0-9]+/[0-9a-f]+$')


def wait_lb():
    waiter = elbv2_cli.get_waiter('load_balancer_available')
    waiter.wait(Names=[LB_NAME])


def get_lb_arn_dns():
    lbs = elbv2_cli.describe_load_balancers(Names=[LB_NAME])
    if len(lbs['LoadBalancers']) == 0:
        raise RuntimeError(f"Load balancer {LB_NAME} not found")
    lb = lbs['LoadBalancers'][0]
    lb_arn = lb.get('LoadBalancerArn')
    if lb_arn is None:
        raise RuntimeError('Load balancer ARN not found')
    lb_dns = lb.get('DNSName')
    if lb_dns is None:
        raise RuntimeError('Load balancer DNS name not found')
    return lb_arn, lb_dns


def specifier_from_arn(arn: str):
    search = SPECIFIER_RE.search(arn)
    if search is None:
        raise RuntimeError(f"Could not match specifier regex in {arn}")
    return search.group()
