import logging

from deploy.bootstrap import bootstrap_instance
from deploy.config import LOG_LEVEL
from deploy.infra import setup_infra

logger = logging.getLogger(__name__)


def main():
    logger.info('Setting up infrastructure')
    instances = setup_infra()

    # Use this to use existing instance instead of creating new ones
    # instances = ec2_res.instances.filter(
    #     Filters=[
    #         {'Name': 'tag:Name', 'Values': [AWS_RES_NAME]},
    #         {'Name': 'instance-state-name', 'Values': ['pending', 'running']},
    #     ]
    # )

    logger.info('Bootstrapping instances')
    for i, inst in enumerate(instances):
        bootstrap_instance(inst, i)


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    main()
