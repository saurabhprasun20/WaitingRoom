import boto3

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)


def increase_assignment_count(hit_Id, increase_count):
    response = client.create_additional_assignments_for_hit(
        HITId=hit_Id,
        NumberOfAdditionalAssignments=increase_count,
    )

    return response

# increase_assignment_count('3GONHBMNI5CY21208DW90D24YN0MZQ',1)
