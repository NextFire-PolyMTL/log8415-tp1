import logging
from datetime import datetime

import orjson

from bench.utils import cw_cli, specifier_from_arn

logger = logging.getLogger(__name__)


def analyze(lb_arn: str, start_time: datetime, end_time: datetime):
    data = _get_all_metric_data(lb_arn, start_time, end_time)
    with open(f'./results/{start_time}.json', 'wb') as f:
        dump = orjson.dumps(data)
        f.write(dump)


def _get_all_metric_data(lb_arn, start_time, end_time):
    specifier = specifier_from_arn(lb_arn)
    metrics = cw_cli.list_metrics(
        Namespace='AWS/ApplicationELB',
        Dimensions=[
            {
                'Name': 'LoadBalancer',
                'Value': specifier
            },
        ],
    )
    data = cw_cli.get_metric_data(
        MetricDataQueries=[{
            'Id': f'metric_{i}',
            'MetricStat': {
                'Metric': metric,
                'Period': 60,
                'Stat': 'Average',
            }
        } for i, metric in enumerate(metrics['Metrics'])],
        StartTime=start_time,
        EndTime=end_time,
    )
    return data['MetricDataResults']
