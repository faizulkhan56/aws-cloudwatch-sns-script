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
   


