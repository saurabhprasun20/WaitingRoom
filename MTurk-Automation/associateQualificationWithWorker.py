import boto3,os,csv

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
# endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

with open(os.path.dirname(__file__) + "/" + "worker.csv", 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        workerId = row['workerId']
        response = client.associate_qualification_with_worker(
            QualificationTypeId="3E5HMETZCUZTBEUSSOPS5NT65QV4VI",
            WorkerId=workerId,
            IntegerValue=60,
            SendNotification=False
        )

        print(response)
