import boto3

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
#endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

response = client.create_qualification_type(
    Name='Human cloning - Please take the reimbursement survey',
    Keywords='survey',
    Description='Please take the survey to reimburse the money for the last survey conducted by Digidem Lab on human '
                'cloning. The HIT-link is - ',
    QualificationTypeStatus='Active',
    RetryDelayInSeconds=16000,
)

print(response)
