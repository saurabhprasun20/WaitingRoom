from datetime import datetime

import boto3, json

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

f = open('../Flask-Server/data.json')
data = json.load(f)
hit_id = data['hitId']

response = client.update_expiration_for_hit(
    HITId=hit_id,
    ExpireAt=datetime(2022, 2, 6, 23, 55, 59)
)