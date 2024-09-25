import json
import boto3

# Load the configuration from the JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Extract parameters from JSON
namespace = config['namespace']  # Custom namespace
metric_name = config['metric_name']  # Custom metric name
alarm_name = config['alarm_name']  # Alarm name
threshold = config['threshold']  # Threshold for the alarm
sns_topic_arn = config['sns_topic_arn']  # SNS topic ARN

# Initialize CloudWatch client
cloudwatch_client = boto3.client('cloudwatch')

# Create a CloudWatch Alarm based on the metric
cloudwatch_client.put_metric_alarm(
    AlarmName=alarm_name,  # Alarm name from JSON
    AlarmDescription=f"Alarm when {metric_name} exceeds {threshold}",
    ActionsEnabled=True,
    MetricName=metric_name,
    Namespace=namespace,
    Statistic='Sum',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-0cefdc359e8944d84'  # Replace with your instance ID or other relevant dimension
        }
    ],
    Period=300,  # 5 minutes
    EvaluationPeriods=1,
    Threshold=threshold,  # Threshold from JSON
    ComparisonOperator='GreaterThanThreshold',
    AlarmActions=[sns_topic_arn]  # SNS topic ARN from JSON
)

print(f"Alarm '{alarm_name}' created successfully!")
