from datetime import datetime, timedelta
from Increase_Assignment import increase_assignment_count

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
print(hit_id)
increase_count = data['minimumNoOfUser']
print(increase_count)

datetime_object = datetime.now()
print("current time is:")
print(datetime_object)
extra_min = 30
expire_time = datetime_object + timedelta(minutes=extra_min)
print("Time to expire is: ")
print(expire_time)

response = client.update_expiration_for_hit(
    HITId=hit_id,
    # ExpireAt=expire_time
    ExpireAt=datetime.timestamp(expire_time)
)

print("Increase time response is: ")
print(response)

response_assignment = increase_assignment_count(hit_id, increase_count)
print("Increase in count response is : ")
print(response_assignment)

with open("../Flask-Server/data.json", "r+") as jsonFile:
    data = json.load(jsonFile)
    data['cycleChange'] = 1
    jsonFile.seek(0)  # rewind
    json.dump(data, jsonFile)
    jsonFile.truncate()
