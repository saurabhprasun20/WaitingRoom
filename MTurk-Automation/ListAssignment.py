import boto3,csv,os

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

response = client.list_assignments_for_hit(
    HITId='3GONHBMNI5CY21208DW90D24YN0MZQ'
    # AssignmentStatuses=["Submitd"]
)

print(response)
assignment_list = response['Assignments']
print(assignment_list)
for i in range(0, len(assignment_list)):
    sibB = os.path.join(os.path.dirname(__file__), '..', 'Flask-Server')
    with open(os.path.join(sibB,"complete_list.csv"), 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([assignment_list[i]['WorkerId'], assignment_list[i]['HITId']])
