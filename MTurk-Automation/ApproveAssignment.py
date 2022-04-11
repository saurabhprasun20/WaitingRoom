import boto3,csv

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

with open("approve_assignment.csv", 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['assignmentId'])
        requester_feedback = ''
        override_rejection = False

        if row['requesterFeedback'] != '':
            requester_feedback = row['requesterFeedback']
            print(requester_feedback)

        if row['overrideRejection'] == 'True':
            override_rejection = True
            print(override_rejection)

        response = client.approve_assignment(
            AssignmentId=row['assignmentId'],
            RequesterFeedback=requester_feedback,
            OverrideRejection=override_rejection
        )