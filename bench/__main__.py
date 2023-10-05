import logging

from bench.config import LOG_LEVEL
from bench.utils import get_lb_arn_dns

logger = logging.getLogger(__name__)


def main():
    lb_arn, lb_dns = get_lb_arn_dns()
    logger.info(f"{(lb_arn, lb_dns)=}")


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    main()
