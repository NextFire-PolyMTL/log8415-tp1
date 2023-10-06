import boto3
import os
from datetime import date, timedelta, datetime, timezone
import json
import os
import logging

logger = logging.getLogger(__name__)

def save_data(json_file_name, data):

    logger.info(data)

    dir = json_file_name[:json_file_name.rfind('/')]
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(json_file_name, 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True, default=str)


###################################################################################################################
#                                             Load Balancer CloudWatch metric
###################################################################################################################
def RequestCount_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RequestCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RequestCount',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def ActiveConnectionCount_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_ActiveConnectionCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'ActiveConnectionCount',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def ConsumedLCUs_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_ConsumedLCUs',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'ConsumedLCUs',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def HTTP_Redirect_Count_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_HTTP_Redirect_Count',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'HTTP_Redirect_Count',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def LB_RequestCount_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RequestCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RequestCount',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def RuleEvaluations_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_RuleEvaluations',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'RuleEvaluations',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def ProcessedBytes_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_ProcessedBytes',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'ProcessedBytes',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Bytes'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def HTTPCode_Target_2XX_Count_metric(cloudwatch_client, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_HTTPCode_Target_2XX_Count',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'HTTPCode_Target_2XX_Count',
                        'Dimensions': [
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


###################################################################################################################
#                                             Get metrics
###################################################################################################################

def save_load_balancer_metrics(cloud_watch, load_balancer_arn):
    lbarray = load_balancer_arn.split(':')
    lbstring = lbarray[-1]
    lbarray2 = lbstring.split('/')
    lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]

    # get current time
    now = datetime.now(timezone.utc)
    StartTime = datetime(now.year, now.month, now.day - 1)
    EndTime = datetime(now.year, now.month, now.day + 1)

    # get RequestCount metric
    data = RequestCount_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/request_count_metric.json", data)

    data = ActiveConnectionCount_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/active_connection_count_metric.json", data)

    data = ConsumedLCUs_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/consumed_lcus_metric.json", data)

    data = HTTP_Redirect_Count_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/http_redirect_count_metric.json", data)

    data = LB_RequestCount_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/request_count_metric.json", data)

    data = RuleEvaluations_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/rule_evaluations_metric.json", data)

    data = ProcessedBytes_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/processed_bytes_metric.json", data)

    data = HTTPCode_Target_2XX_Count_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/http_code_target_2xx_metric.json", data)