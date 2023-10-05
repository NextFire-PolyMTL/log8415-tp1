import logging
from datetime import datetime
from time import sleep

from bench.analysis import analyze
from bench.config import LOG_LEVEL
from bench.scenarios import run_scenarios
from bench.utils import get_lb_arn_dns, wait_lb

logger = logging.getLogger(__name__)


def main():
    wait_lb()
    lb_arn, lb_dns = get_lb_arn_dns()
    logger.info(f"{(lb_arn, lb_dns)=}")

    logger.info(
        'Sleeping for 60 seconds to avoid overlapping metrics with previous runs')
    sleep(60)

    start_time = datetime.utcnow()
    for cluster in ('cluster1', 'cluster2'):
        run_scenarios(lb_dns, cluster)
    end_time = datetime.utcnow()

    logger.info('Starting analysis')
    analyze(lb_arn, start_time, end_time)

    logger.info('Done. Please check the contents of the `./results` directory.')


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    main()
