import boto3

# Initialize CloudWatch client (SNS client removed since we're not creating SNS here)
cloudwatch = boto3.client('cloudwatch')

# Manually provide the SNS Topic ARN
sns_topic_arn = 'arn:aws:sns:us-east-1:149451857623:cpu-alarm-topic'  # Replace with your actual SNS Topic ARN
print(f"Using SNS Topic ARN: {sns_topic_arn}")

# Step 1: Create CloudWatch Alarm for CPU Utilization
response = cloudwatch.put_metric_alarm(
    AlarmName='High_CPU_Utilization',
    AlarmDescription='Alarm when CPU exceeds 80%',
    ActionsEnabled=True,
    AlarmActions=[sns_topic_arn],  # Use the manually provided SNS topic ARN for notifications
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-0cefdc359e8944d84'  # Replace with your actual EC2 instance ID
        }
    ],
    Period=300,  # Period in seconds (5 minutes)
    EvaluationPeriods=1,
    Threshold=80.0,
    ComparisonOperator='GreaterThanThreshold',
    TreatMissingData='breaching'
)

print("CloudWatch Alarm created successfully!")
