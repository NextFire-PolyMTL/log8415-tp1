import logging
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import orjson

from bench.config import CLUSTER_1_TARGET_NAME, CLUSTER_2_TARGET_NAME
from bench.constants import GRAPH_INFO
from bench.utils import cw_cli, specifier_from_arn

if TYPE_CHECKING:
    from mypy_boto3_cloudwatch.type_defs import (
        DimensionTypeDef,
        MetricDataResultTypeDef,
    )

logger = logging.getLogger(__name__)


def analyze(lb_arn: str,
            start_time: datetime,
            end_time: datetime,
            tg_arn: str | None = None):
    data, path = _save_metrics_data(
        lb_arn, start_time, end_time, tg_arn=tg_arn)
    _generate_graph(data, tg_arn)


def _generate_graph(data: list['MetricDataResultTypeDef'], tg_arn: str | None = None):
    for item in data:
        label = item.get('Label')
        timestamps = item.get('Timestamps')
        values = item.get('Values')

        if label is None or timestamps is None or values is None:
            raise ValueError(
                f"Missing label, timestamps or values for {item=}")

        active_connection_timestamps = list(
            map(lambda t: t.strftime(r'%Y-%m-%d %H:%M'), reversed(timestamps)))
        active_connection_values = list(reversed(values))

        if len(active_connection_timestamps) > 0:
            x_axis = np.arange(len(timestamps))
            _create_graph(active_connection_timestamps,
                          active_connection_values,
                          x_axis,
                          label,
                          tg_arn)


def _addLabels(x: list[str], y: list[float]):
    """Add value labels in the graph"""
    for i in range(len(x)):
        plt.text(i, y[i], str(y[i]), ha='center')


def _create_graph(abscissa: list[str],
                  ordinate: list[float],
                  x_axis: np.ndarray,
                  itemLabel: str,
                  tg_arn: str | None = None):
    fig = plt.figure(figsize=(10, 10))
    # fig.suptitle(GRAPH_INFO[itemLabel]['TITLE'])
    ax = fig.add_subplot(111)
    ax.bar(abscissa, ordinate)
    ax.set_xticklabels(abscissa, rotation=45)
    _addLabels(abscissa, ordinate)
    plt.xlabel(GRAPH_INFO[itemLabel]['XLABEL'])
    plt.ylabel(GRAPH_INFO[itemLabel]['YLABEL'])
    plt.plot(x_axis, ordinate, color="red")

    suffix = _target_group_name_from_arn(tg_arn)

    plt.savefig(f"./results/figures/{suffix}_{itemLabel}.pdf", dpi=400)
    # plt.show()


def _target_group_name_from_arn(tg_arn: str | None):
    if tg_arn is None:
        tg_name = 'load_balancer'
    elif CLUSTER_1_TARGET_NAME in tg_arn:
        tg_name = 'tg1'
    elif CLUSTER_2_TARGET_NAME in tg_arn:
        tg_name = 'tg2'
    else:
        raise ValueError(f"Unknown target group: {tg_arn}")
    return tg_name


def _save_metrics_data(lb_arn: str,
                       start_time: datetime,
                       end_time: datetime,
                       tg_arn: str | None = None):
    data = _get_metric_data(lb_arn, start_time, end_time, tg_arn)
    base_dir = Path(f'./results/{start_time}')
    if not base_dir.exists():
        os.mkdir(base_dir)
    filename = (f"{tg_arn.replace('/', '_')}.json"
                if tg_arn is not None else 'load_balabcer.json')
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
                'ReturnData': True,
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
                'ReturnData': True,
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
                'ReturnData': True,
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
                'ReturnData': True,
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
                'ReturnData': True,
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
                'ReturnData': True,
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
                'ReturnData': True,
            },
            {
                'Id': 'myrequest_HealthyHostCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'HealthyHostCount',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Average',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
            {
                'Id': 'myrequest_TargetConnectionErrorCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'TargetConnectionErrorCount',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
            {
                'Id': 'myrequest_TargetResponseTime',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'TargetResponseTime',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Average',
                    'Unit': 'Seconds'
                },
                'ReturnData': True,
            },
            {
                'Id': 'myrequest_UnHealthyHostCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'UnHealthyHostCount',
                        'Dimensions': dimensions
                    },
                    'Period': 60,
                    'Stat': 'Average',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    return data['MetricDataResults']
