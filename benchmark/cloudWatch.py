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
#                                             Load Balancer CloudWatch metrics
###################################################################################################################
def request_count_metric(cloudwatch_client, lbstring, StartTime, EndTime):
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


def active_connection_count_metric(cloudwatch_client, lbstring, StartTime, EndTime):
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


def consumed_LCUs_metric(cloudwatch_client, lbstring, StartTime, EndTime):
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


def http_redirect_count_metric(cloudwatch_client, lbstring, StartTime, EndTime):
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


def lb_request_count_metric(cloudwatch_client, lbstring, StartTime, EndTime):
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


def rule_evaluations_metric(cloudwatch_client, lbstring, StartTime, EndTime):
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


def processed_bytes_metric(cloudwatch_client, lbstring, StartTime, EndTime):
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


def http_code_target_2XX_count_metric(cloudwatch_client, lbstring, StartTime, EndTime):
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
#                                             Save Load balancer metrics
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
    data = request_count_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/request_count_metric.json", data)

    data = active_connection_count_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/active_connection_count_metric.json", data)

    data = consumed_LCUs_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/consumed_lcus_metric.json", data)

    data = http_redirect_count_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/http_redirect_count_metric.json", data)

    data = lb_request_count_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/request_count_metric.json", data)

    data = rule_evaluations_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/rule_evaluations_metric.json", data)

    data = processed_bytes_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/processed_bytes_metric.json", data)

    data = http_code_target_2XX_count_metric(cloud_watch, lbstring=lbstring2, StartTime=StartTime, EndTime=EndTime)
    save_data("metrics/cloudwatch/load_balancer/http_code_target_2xx_metric.json", data)

    print("Enregistrement des metrics du Load balancer dans CloudWatch :::: done ....")



###################################################################################################################
#                                             Targets CloudWatch metrics
###################################################################################################################

def healthy_host_count_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_HealthyHostCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'HealthyHostCount',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def request_count_per_target_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
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
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
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


def target_connection_error_count_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_TargetConnectionErrorCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'TargetConnectionErrorCount',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
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


def target_response_time_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_TargetResponseTime',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'TargetResponseTime',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                    'Unit': 'Seconds'
                },
                'ReturnData': True,
            },
        ],
        StartTime=StartTime,
        EndTime=EndTime,
    )

    return response


def unhealthy_host_count_metric(cloudwatch_client, tgstring, lbstring, StartTime, EndTime):
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'myrequest_UnHealthyHostCount',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'UnHealthyHostCount',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': tgstring
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': lbstring
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
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
#                                             Save Targets metrics
###################################################################################################################

def save_targets_metrics(cloud_watch, target_group_arn, load_balancer_arn, target_grp_number):
    print("Start saving targets CloudWatch metrics ....")

    tgarray = target_group_arn.split(':')
    tgstring = tgarray[-1]

    lbarray = load_balancer_arn.split(':')
    lbstring = lbarray[-1]
    lbarray2 = lbstring.split('/')
    lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]

    now = datetime.now(timezone.utc)
    StartTime = datetime(now.year, now.month, now.day - 1)
    EndTime = datetime(now.year, now.month, now.day + 1)

    data = healthy_host_count_metric(cloud_watch, tgstring=tgstring, lbstring=lbstring2, StartTime=StartTime,
                                   EndTime=EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/healthy_host_count_metric.json", data)

    data = request_count_per_target_metric(cloud_watch, tgstring=tgstring, lbstring=lbstring2, StartTime=StartTime,
                                        EndTime=EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/request_count_per_target_metric.json", data)

    data = target_connection_error_count_metric(cloud_watch, tgstring=tgstring, lbstring=lbstring2, StartTime=StartTime,
                                             EndTime=EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/target_connection_error_count_metric.json",
              data)

    data = target_response_time_metric(cloud_watch, tgstring=tgstring, lbstring=lbstring2, StartTime=StartTime,
                                     EndTime=EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/target_response_time_metric.json", data)

    data = unhealthy_host_count_metric(cloud_watch, tgstring=tgstring, lbstring=lbstring2, StartTime=StartTime,
                                     EndTime=EndTime)
    save_data("cloudwatch/targets/target_grp_" + str(target_grp_number) + "/unhealthy_host_count_metric.json", data)

    print("Enregistrement des metrics des Targets dans CloudWatch :::: done ....")
