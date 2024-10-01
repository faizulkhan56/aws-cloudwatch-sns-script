import json
import boto3
import time

# Load the configuration from the config.json file
with open('config.json') as config_file:
    config = json.load(config_file)

# Initialize AWS CloudWatch and Logs clients
cloudwatch_client = boto3.client('cloudwatch')
logs_client = boto3.client('logs')

# Helper function to create or update metric-based alarms
def create_metric_alarm(alarm):
    alarm_name = alarm['alarm_name']
    metric_name = alarm['metric_name']
    namespace = alarm['namespace']
    threshold = alarm['threshold']
    sns_topic_arn = alarm['sns_topic_arn']
    evaluation_periods = alarm.get('evaluation_periods', 1)
    period = alarm.get('period', 300)
    comparison_operator = alarm.get('comparison_operator', 'GreaterThanThreshold')

    # Create or update the CloudWatch Metric Alarm
    cloudwatch_client.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription=f"Alarm when {metric_name} exceeds {threshold}",
        ActionsEnabled=True,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic='Sum',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0cefdc359e8944d84'  # Replace with relevant dimension
            }
        ],
        Period=period,
        EvaluationPeriods=evaluation_periods,
        Threshold=threshold,
        ComparisonOperator=comparison_operator,
        AlarmActions=[sns_topic_arn]
    )
    print(f"Metric alarm '{alarm_name}' created or updated successfully!")

# Helper function to create or update logs-based alarms
def create_logs_based_alarm(alarm):
    alarm_name = alarm['alarm_name']
    log_group_name = alarm['log_group_name']
    query_string = alarm['query']
    namespace = alarm['namespace']
    metric_name = alarm['metric_name']
    threshold = alarm['threshold']
    sns_topic_arn = alarm['sns_topic_arn']
    start_time_offset = alarm.get('start_time_offset_in_seconds', 3600)
    end_time_offset = alarm.get('end_time_offset_in_seconds', 0)

    # Start the CloudWatch Logs Insights query
    current_time = int(time.time())
    start_time = current_time - start_time_offset
    end_time = current_time - end_time_offset

    response = logs_client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString=query_string,
        limit=1000
    )
    
    query_id = response['queryId']

    # Poll until the query completes
    while True:
        response = logs_client.get_query_results(queryId=query_id)
        if response['status'] == 'Complete':
            break
        time.sleep(1)

    # Count the number of results from the query
    result_count = len(response['results'])

    # Put the metric data into CloudWatch using the custom namespace and metric name
    cloudwatch_client.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': metric_name,
                'Dimensions': [
                    {
                        'Name': 'InstanceId',
                        'Value': 'i-0cefdc359e8944d84'  # Replace with relevant dimension
                    }
                ],
                'Unit': 'Count',
                'Value': result_count  # The number of query results
            }
        ]
    )

    # Now create the alarm based on the custom metric
    cloudwatch_client.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription=f"Alarm when {metric_name} exceeds {threshold}",
        ActionsEnabled=True,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic='Sum',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0cefdc359e8944d84'  # Replace with relevant dimension
            }
        ],
        Period=300,  # 5 minutes
        EvaluationPeriods=1,
        Threshold=threshold,
        ComparisonOperator='GreaterThanThreshold',
        AlarmActions=[sns_topic_arn]
    )
    print(f"Logs-based alarm '{alarm_name}' created or updated successfully!")

# Loop through each alarm configuration in config.json
for alarm in config['alarms']:
    if alarm['type'] == 'metric':
        create_metric_alarm(alarm)
    elif alarm['type'] == 'logs':
        create_logs_based_alarm(alarm)
