import boto3, csv, os

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

current_dir= os.path.join(os.path.dirname(__file__))
with open(os.path.join(current_dir,"reject_assignment.csv"), 'r', newline='') as file:
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
