import boto3, csv

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

with open("reject_assignment.csv", 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['assignmentId'])
        requester_feedback = ''

        if row['requesterFeedback'] != '':
            requester_feedback = row['requesterFeedback']
            print(requester_feedback)

        response = client.reject_assignment(
            AssignmentId=row['assignmentId'],
            RequesterFeedback=requester_feedback
        )
