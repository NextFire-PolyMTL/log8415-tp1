import logging
from threading import Barrier, Thread
from time import sleep

import requests

logger = logging.getLogger(__name__)

barrier = Barrier(2)


def run_scenarios(lb_dns: str, cluster: str):
    barrier.reset()
    thread1 = Thread(target=scenario1, args=(lb_dns, cluster))
    thread2 = Thread(target=scenario2, args=(lb_dns, cluster))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


def scenario1(lb_dns: str, cluster: str):
    logger.info(f"Starting scenario 1 on {cluster}")
    barrier.wait()
    for _ in range(1000):
        _make_req(lb_dns, cluster)
    logger.info(f"Finished scenario 1 on {cluster}")


def scenario2(lb_dns: str, cluster: str):
    logger.info(f"Starting scenario 2 on {cluster}")
    barrier.wait()
    for _ in range(500):
        _make_req(lb_dns, cluster)
    sleep(60)
    for _ in range(1000):
        _make_req(lb_dns, cluster)
    logger.info(f"Finished scenario 2 on {cluster}")


def _make_req(lb_dns, cluster):
    requests.get(f"http://{lb_dns}/{cluster}")
