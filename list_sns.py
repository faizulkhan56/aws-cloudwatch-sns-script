import boto3

# Initialize the SNS client
sns_client = boto3.client('sns')

def list_all_sns_topics():
    """List all SNS topics, handling pagination."""
    topics = []
    next_token = None

    while True:
        if next_token:
            response = sns_client.list_topics(NextToken=next_token)
        else:
            response = sns_client.list_topics()

        topics.extend(response['Topics'])

        # Check if there is another page of results
        next_token = response.get('NextToken')
        if not next_token:
            break

    return topics

def list_all_sns_subscriptions():
    """List all SNS subscriptions, handling pagination."""
    subscriptions = []
    next_token = None

    while True:
        if next_token:
            response = sns_client.list_subscriptions(NextToken=next_token)
        else:
            response = sns_client.list_subscriptions()

        subscriptions.extend(response['Subscriptions'])

        # Check if there is another page of results
        next_token = response.get('NextToken')
        if not next_token:
            break

    return subscriptions

if __name__ == '__main__':
    # List and print SNS topics
    print("Listing all SNS Topics:")
    topics = list_all_sns_topics()
    for topic in topics:
        print(f"Topic ARN: {topic['TopicArn']}")

    # List and print SNS subscriptions
    print("\nListing all SNS Subscriptions:")
    subscriptions = list_all_sns_subscriptions()
    for sub in subscriptions:
        print(f"Subscription ARN: {sub['SubscriptionArn']} (Topic ARN: {sub['TopicArn']})")

