import json
import urllib3
import os

http = urllib3.PoolManager()

def lambda_handler(event, context):
    # The Slack webhook URL to which the message will be sent
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    
    # Parse the SNS message
    sns_message = event['Records'][0]['Sns']['Message']
    
    # Format the message for Slack
    slack_message = {
        "text": f"CloudWatch Alarm Triggered: {sns_message}"
    }
    
    # Send the message to Slack
    response = http.request(
        'POST',
        slack_webhook_url,
        body=json.dumps(slack_message),
        headers={'Content-Type': 'application/json'}
    )
    
    # Check the response
    if response.status == 200:
        return {
            'statusCode': 200,
            'body': json.dumps('Message sent to Slack successfully')
        }
    else:
        return {
            'statusCode': response.status,
            'body': json.dumps(f'Failed to send message to Slack: {response.data}')
        }

