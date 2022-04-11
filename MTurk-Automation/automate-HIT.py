import boto3, json, csv
import xml.etree.ElementTree as ET
from datetime import datetime

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

f = open('../Flask-Server/data.json')
data = json.load(f)


# This code is to update the question link.
question_tree = ET.parse("question.xml")
rootElement = question_tree.getroot()
for child in rootElement.findall('{http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14'
                                 '/ExternalQuestion.xsd}ExternalURL'):
    child.text = data['question']

question_tree.write("question.xml", encoding='UTF-8', xml_declaration=True)
##
f.close()

# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])

question = open('question.xml', 'r').read()
new_hit = client.create_hit(
    # Title='Online survey for Political science department conducted by the University of Zurich',
    Title="Test--1",
    Description='Qualtrics Survey with restriction',
    Keywords='text, quick, labeling',
    Reward='0.15',
    MaxAssignments=1,
    LifetimeInSeconds=300,
    AssignmentDurationInSeconds=1800,
    AutoApprovalDelayInSeconds=14400,
    Question=question,
    # QualificationRequirements=[
    #     {
    #         'QualificationTypeId': '000000000000000000L0',
    #         'Comparator': 'GreaterThanOrEqualTo',
    #         'IntegerValues': [75],
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
print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")

with open("history.csv", 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([new_hit['HIT']['HITId'], datetime.now()])

with open("../Flask-Server/data.json", "r+") as jsonFile:
    data = json.load(jsonFile)
    data["hitId"] = new_hit['HIT']['HITId']
    jsonFile.seek(0)  # rewind
    json.dump(data, jsonFile)
    jsonFile.truncate()
