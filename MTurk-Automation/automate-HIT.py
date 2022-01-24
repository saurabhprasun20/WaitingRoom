import boto3

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])

question = open('question.xml', 'r').read()
new_hit = client.create_hit(
    Title='Online survey for Political science department',
    Description='Qualtrics Survey with restriction',
    Keywords='text, quick, labeling',
    Reward='0.15',
    MaxAssignments=1,
    LifetimeInSeconds=1800,
    AssignmentDurationInSeconds=600,
    AutoApprovalDelayInSeconds=14400,
    Question=question,
    QualificationRequirements=[
        {
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [75],
        },
        {
            'QualificationTypeId': '00000000000000000071',
            'Comparator': 'In',
            'LocaleValues': [
                {'Country': 'US'},
            ]
        }
    ],
)
print("A new HIT has been created. You can preview it here:")
print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
