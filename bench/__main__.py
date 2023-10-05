import logging

from bench.config import LOG_LEVEL
from bench.scenarios import run_scenarios
from bench.utils import get_lb_arn_dns, wait_lb

logger = logging.getLogger(__name__)


def main():
    wait_lb()
    lb_arn, lb_dns = get_lb_arn_dns()
    logger.info(f"{(lb_arn, lb_dns)=}")
    run_scenarios(lb_dns, 'cluster1')
    run_scenarios(lb_dns, 'cluster2')


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    main()
