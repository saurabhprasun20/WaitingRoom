import boto3

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)


response = client.get_hit(
    HITId='3RTFSSG7UIKA2OFAXEBN1WTXGCLLW3'
)

print(response)


response1 = client.list_hits()

print("Listing all --->")
print()
print(response1)