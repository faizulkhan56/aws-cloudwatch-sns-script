import boto3

# Initialize SNS and CloudWatch clients
sns = boto3.client('sns')
cloudwatch = boto3.client('cloudwatch')

# Step 1: Create SNS Topic
response = sns.create_topic(Name='cpu-alarm-topic')
sns_topic_arn = response['TopicArn']
print(f"SNS Topic created: {sns_topic_arn}")

# Step 2: Subscribe to the SNS Topic
email = 'faizulkhan56@gmail.com'
sns.subscribe(
    TopicArn=sns_topic_arn,
    Protocol='email',
    Endpoint=email
)
print(f"Subscription created for {email}")

# Step 3: Create CloudWatch Alarm for CPU Utilization
response = cloudwatch.put_metric_alarm(
    AlarmName='High_CPU_Utilization',
    AlarmDescription='Alarm when CPU exceeds 80%',
    ActionsEnabled=True,
    AlarmActions=[sns_topic_arn],  # Send notifications to the SNS topic
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-08f45a96a9a7d5167'  # Replace with your second EC2 instance ID
        }
    ],
    Period=300,  # Period in seconds (5 minutes)
    EvaluationPeriods=1,
    Threshold=80.0,
    ComparisonOperator='GreaterThanThreshold',
    TreatMissingData='breaching'
)

print("CloudWatch Alarm created successfully!")
