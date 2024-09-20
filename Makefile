# Variables
VENV=venv
PYTHON=$(VENV)/bin/python

# Target to run the create SNS and CloudWatch alarm script
create_alarm:
	$(PYTHON) create_alarm.py

# Target to run the list SNS topics and subscriptions script
list_sns:
	$(PYTHON) list_sns.py

# Target to run both scripts (default target)
all: create_alarm list_sns