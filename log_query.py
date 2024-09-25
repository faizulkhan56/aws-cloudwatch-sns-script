import json
import boto3
import time


with open('config.json') as config_file:
    config = json.load(config_file)

# Extract parameters from JSON
log_group_name = config['log_group_name']
query_string = config['query']
start_time_offset_in_hours = config.get('start_time_offset_in_hours', 1)
limit = config.get('limit', 1000)

# Initialize CloudWatch Logs client
logs_client = boto3.client('logs')

# Start the CloudWatch Logs Insights query
response = logs_client.start_query(
    logGroupName=log_group_name,
    startTime=int(time.time() - start_time_offset_in_hours * 60 * 60),  # Offset based on JSON value
    endTime=int(time.time()),  # Until now
    queryString=query_string,
    limit=limit
)

query_id = response['queryId']

# Poll until the query completes
while True:
    response = logs_client.get_query_results(queryId=query_id)
    if response['status'] == 'Complete':
        break
    time.sleep(1)

# Display the query results
if response['results']:
    print("Query Results:")
    for result in response['results']:
        for field in result:
            print(f"{field['field']}: {field['value']}")
else:
    print("No results found.")