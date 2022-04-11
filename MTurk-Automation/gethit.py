import boto3

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)


response = client.get_hit(
    HITId='344M16OZLST69OW4ORXWSIQMF72NEM'
)

print(response)
