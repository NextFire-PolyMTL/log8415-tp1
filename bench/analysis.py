import logging
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import orjson
import json
import numpy as np
import matplotlib.pyplot as pyplot

from bench.constants import *

from bench.utils import cw_cli, specifier_from_arn

if TYPE_CHECKING:
    from mypy_boto3_cloudwatch.type_defs import DimensionTypeDef

logger = logging.getLogger(__name__)


def analyze(lb_arn: str,
            start_time: datetime,
            end_time: datetime,
            tg_arn: str | None = None):
    data, path = _save_metrics_data(lb_arn, start_time, end_time, tg_arn)
    _generate_graph(path, tg_arn)


def _generate_graph(path, tg_arn: str | None = None):
    with open(path, 'r') as f:
      data = json.load(f)

    for item in data:
        timeStamps = item.get('Timestamps')
        values = item.get('Values')

        active_connection_timestamps = list(reversed(timeStamps)) 
        active_connection_values = list(reversed(values)) 
        x_axis = np.arange(len(timeStamps))
        if active_connection_timestamps not in [None, []]:
            _create_graph(active_connection_timestamps, active_connection_values, x_axis, item.get('Label'), tg_arn)


# function to add value labels in the graph
def _addLabels(pyplot, x,y):
    for i in range(len(x)):
        pyplot.text(i, y[i], y[i], ha = 'center')

def _create_graph(abscissa, ordinate, x_axis, itemLabel, tg_arn: str | None = None):
    fig = pyplot.figure(figsize=(10,10))
    #fig.suptitle(GRAPH_INFO[itemLabel]['TITLE'])
    ax = fig.add_subplot(111)
    ax.bar(abscissa, ordinate)
    ax.set_xticklabels(abscissa,rotation = 45)
    _addLabels(pyplot,abscissa, ordinate)
    pyplot.xlabel(GRAPH_INFO[itemLabel]['XLABEL'])
    pyplot.ylabel(GRAPH_INFO[itemLabel]['YLABEL'])
    pyplot.plot(x_axis, ordinate, color="red")
    
    suffix = _target_group_name_from_arn(tg_arn)

    pyplot.savefig(f"./results/figures/{suffix}_{itemLabel}.pdf", dpi=400)
   # pyplot.show()


def _target_group_name_from_arn(tg_arn):
    tg_name = 'load_balancer'
    if tg_arn is not None and 'Lab1-1' in tg_arn:
        tg_name = 'tg1'
    elif tg_arn is not None and 'Lab1-2' in tg_arn:
         tg_name = 'tg2'
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
