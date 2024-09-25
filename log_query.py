import json
import boto3
import time

# Load the configuration from the JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Extract parameters from JSON
log_group_name = config['log_group_name']
query_string = config['query']
namespace = config['namespace']  # Custom namespace
metric_name = config['metric_name']  # Custom metric name
start_time_offset_in_seconds = config.get('start_time_offset_in_seconds', 3600)  # Default: 1 hour ago
end_time_offset_in_seconds = config.get('end_time_offset_in_seconds', 0)  # Default: now

# Initialize CloudWatch Logs and CloudWatch clients
logs_client = boto3.client('logs')
cloudwatch_client = boto3.client('cloudwatch')

# Calculate startTime and endTime for the query
current_time = int(time.time())
start_time = current_time - start_time_offset_in_seconds
end_time = current_time - end_time_offset_in_seconds

# Start the CloudWatch Logs Insights query
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
    Namespace=namespace,  # Custom namespace from JSON
    MetricData=[
        {
            'MetricName': metric_name,  # Custom metric name from JSON
            'Dimensions': [
                {
                    'Name': 'InstanceId',
                    'Value': 'i-0cefdc359e8944d84'  # Replace with your instance ID or other relevant dimension
                }
            ],
            'Unit': 'Count',
            'Value': result_count  # The number of query results
        }
    ]
)

print(f"Metric '{metric_name}' updated with value: {result_count}")
