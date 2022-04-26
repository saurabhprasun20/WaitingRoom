import boto3, json, csv, os
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Flask-Server'))
from randomChat import select_chat_room


region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
#endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
preview_url = "https://workersandbox.mturk.com/mturk/preview"
#preview_url = "https://www.mturk.com/mturk/preview"

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

data={}
sibB = os.path.join(os.path.dirname(__file__), '..', 'Flask-Server')
for filename in os.listdir(sibB):
    if filename == 'data.json':
        f = open(os.path.join(sibB,filename))
        data = json.load(f)
        print(data)


# This code is to update the question link.
question_tree = ET.parse(os.path.dirname(__file__)+"/"+"question.xml")
rootElement = question_tree.getroot()
for child in rootElement.findall('{http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14'
                                 '/ExternalQuestion.xsd}ExternalURL'):
    child.text = data['question']

question_tree.write(os.path.dirname(__file__)+"/"+"question.xml", encoding='UTF-8', xml_declaration=True)
##
f.close()

# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])

question = open(os.path.dirname(__file__)+"/"+'question.xml', 'r').read()
new_hit = client.create_hit(
    # Title='Online survey for Political science department conducted by the University of Zurich',
    Title='Participate in a survey about human cloning',
    Description='Answer a survey about human cloning and participate in an online chatroom to talk about human cloning',
    Keywords='survey, chatroom, cloning',
    Reward='3.5',
    MaxAssignments=50,
    LifetimeInSeconds=300,
    AssignmentDurationInSeconds=1800,
    AutoApprovalDelayInSeconds=432000,
    Question=question,
    # QualificationRequirements=[
    #     {
    #         'QualificationTypeId': '000000000000000000L0',
    #         'Comparator': 'GreaterThanOrEqualTo',
    #         'IntegerValues': [90],
    #     },
    #     {
    #         'QualificationTypeId': '00000000000000000071',
    #         'Comparator': 'In',
    #         'LocaleValues': [
    #             {'Country': 'US'},
    #         ]
    #     }
    # ],
)
print("A new HIT has been created. You can preview it here:")
print(preview_url+"?groupId=" + new_hit['HIT']['HITGroupId'])
print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")

with open(os.path.dirname(__file__)+"/"+"history.csv", 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([new_hit['HIT']['HITId'], datetime.now()])

for filename in os.listdir(sibB):
    if filename == 'data.json':
        with open(os.path.join(sibB,filename), "r+") as jsonFile:
            data = json.load(jsonFile)
            data["hitId"] = new_hit['HIT']['HITId']
            data['chatRoom'] = select_chat_room()
            jsonFile.seek(0)  # rewind
            json.dump(data, jsonFile)
            jsonFile.truncate()
