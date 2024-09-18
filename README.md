# AWS CloudWatch & SNS Python Script

This repository contains a Python script that creates a CloudWatch alarm for monitoring the CPU utilization of an EC2 instance and sends notifications to an SNS topic. The SNS topic sends email notifications when the alarm triggers.

## Features
- Creates an SNS topic.
- Subscribes an email address to the SNS topic.
- Sets up a CloudWatch alarm to monitor CPU utilization of a specified EC2 instance.
- Sends email notifications via SNS when CPU usage exceeds a specified threshold.

## Prerequisites

Before running the script, make sure you have the following:

1. **AWS Account**: Ensure you have an AWS account with permissions to manage CloudWatch and SNS.
2. **Python 3.x**: Make sure Python is installed on your system. You can install it with:
   ```bash
   sudo apt install python3 python3-pip
   pip3 install boto3
3. **Create an IAM Role (if using EC2)**: If running this script on an EC2 instance, attach an IAM role to your instance with the following permissions:

CloudWatchFullAccess
AmazonSNSFullAccess

4. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/aws-cloudwatch-sns-script.git
   cd aws-cloudwatch-sns-script
   python3 -m venv venv
   source venv/bin/activate
   pip install boto3
   python3 create_alarm.py

5. **Create lambda function for slack notification**:
   a. Create a Slack Webhook URL
      1.Go to your Slack workspace and navigate to the app integrations page: Slack Apps.
      2.Search for Incoming Webhooks and install it.
      3.Set up the Webhook URL by choosing a channel where the messages will be posted.
      4.Once created, you will get a Webhook URL. Copy it, as you will need it in your Lambda function.

   b.Create Lambda Function to Send SNS Messages to Slack
      Here is the Lambda function code (Python 3.9 runtime) that will:

      Receive the SNS message when the CloudWatch alarm triggers.
      Format the message.
      Send it to the Slack channel using the Webhook URL.
   c.Deploy the Lambda Function

     Go to AWS Lambda Console: Create a new Lambda function.

    Runtime: Choose Python 3.9.
   Execution Role: Make sure the role has permissions to execute and log outputs to CloudWatch.
    Add the Environment Variable: After creating the Lambda function, add the Slack Webhook URL as an environment variable.

   Key: SLACK_WEBHOOK_URL
   Value: Your Slack webhook URL (e.g., https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/XXXXXXXXXXXX)
   Paste the Lambda Code: Copy the Python code provided above and paste it into the Lambda editor.

   Test the Function: You can manually test the Lambda by creating a test event with the following structure to simulate an SNS message:

   d.Subscribe Lambda to SNS Topic
   Go to the SNS Console and select the SNS topic you created for CloudWatch alarms.
   In the SNS topic, create a subscription:
   Protocol: Lambda
   Endpoint: Select your Lambda function
   Confirm the subscription.

   e.To test the full setup, simulate high CPU usage or manually trigger the CloudWatch alarm. Once the alarm triggers:

     It sends a message to the SNS topic.
     The SNS topic invokes your Lambda function.
     The Lambda function sends a message to your Slack channel with details about the alarm.

   f.IAM Role and Policies for Lambda


 Permissions for SNS Access
Your Lambda function will be invoked by an SNS topic, so it needs permissions to access SNS. You can attach a policy to allow it to read messages from SNS.

Combined IAM Policy
You can either use the built-in AWS policies or create a custom policy. Here’s what the policies should include:

CloudWatch Logging: This allows Lambda to log to CloudWatch.
SNS Access: This allows Lambda to access SNS (to read messages).
Create an IAM Role for Lambda
Go to the IAM Console and navigate to Roles.
Click on Create role.
Choose a trusted entity: Select Lambda as the trusted entity since this role will be for a Lambda function.
Attach the following policies:

AWS Managed Policy for Lambda Logging:
You can attach the managed policy for CloudWatch logs:

AWSLambdaBasicExecutionRole (allows writing to CloudWatch Logs).
SNS Access Policy (Custom or Managed Policy):
If you want to grant access to SNS for reading messages, create a custom policy or attach an existing

g. Review and create the role, and give it a name like Lambda_SNS_Role.

Attach the role to your Lambda function:

Go to the Lambda Console.
Select your Lambda function.
Under the Configuration tab, choose Execution Role, and attach the IAM role you just created.

h.Add Webhook URL to Your AWS Lambda Function
In your Lambda function, add the Webhook URL as an environment variable for security:

Go to the Lambda Console.
Select your Lambda function.
Under Configuration > Environment Variables, add a new environment variable:
Key: SLACK_WEBHOOK_URL
Value: Your Slack Webhook URL.


   


