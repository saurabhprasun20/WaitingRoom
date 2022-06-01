import boto3

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
# endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

response = client.get_qualification_type(
    QualificationTypeId='3E5HMETZCUZTBEUSSOPS5NT65QV4VI'
)

print(response)
