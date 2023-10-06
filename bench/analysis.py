import logging
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import orjson

from bench.utils import cw_cli, specifier_from_arn

if TYPE_CHECKING:
    from mypy_boto3_cloudwatch.type_defs import DimensionTypeDef

logger = logging.getLogger(__name__)


def analyze(lb_arn: str,
            start_time: datetime,
            end_time: datetime,
            tg_arn: str | None = None):
    data, path = _save_metrics_data(lb_arn, start_time, end_time, tg_arn)


def _save_metrics_data(lb_arn: str,
                       start_time: datetime,
                       end_time: datetime,
                       tg_arn: str | None = None):
    data = _get_metric_data(lb_arn, start_time, end_time, tg_arn)
    base_dir = Path(f'./results/{start_time}')
    if not base_dir.exists():
        os.mkdir(base_dir)
    filename = (f"{tg_arn.replace('/', '_')}.json"
                if tg_arn is not None else 'all.json')
    path = base_dir / filename
    with open(path, 'wb') as f:
        dump = orjson.dumps(data)
        f.write(dump)
    return data, path


def _get_metric_data(lb_arn: str,
                     start_time: datetime,
                     end_time: datetime,
                     tg_arn: str | None = None):
    lb_specifier = specifier_from_arn(lb_arn)
    dimensions: list['DimensionTypeDef'] = [
        {
            'Name': 'LoadBalancer',
            'Value': lb_specifier
        }
    ]
    if tg_arn is not None:
        tg_specifier = specifier_from_arn(tg_arn)
        dimensions.append({
            'Name': 'TargetGroup',
            'Value': tg_specifier
        })
    data = cw_cli.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RequestCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RequestCount',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
            },
            {
                'Id': 'myrequest_ActiveConnectionCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'ActiveConnectionCount',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
            },
            {
                'Id': 'myrequest_ConsumedLCUs',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'ConsumedLCUs',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
            },
            {
                'Id': 'myrequest_HTTP_Redirect_Count',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'HTTP_Redirect_Count',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
            },
            {
                'Id': 'myrequest_RuleEvaluations',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RuleEvaluations',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
            },
            {
                'Id': 'myrequest_ProcessedBytes',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'ProcessedBytes',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Bytes'
                },
            },
            {
                'Id': 'myrequest_HTTPCode_Target_2XX_Count',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'HTTPCode_Target_2XX_Count',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    return data['MetricDataResults']
