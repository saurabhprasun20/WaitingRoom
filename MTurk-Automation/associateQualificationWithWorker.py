import boto3,os,csv

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
# endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)
with open(os.path.dirname(__file__) + "/" + "pendingList1.csv", 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        workerId = row['workerId']
        response = client.associate_qualification_with_worker(
            QualificationTypeId="3HE7BV11M3BWRNG5BB1LW22WU2R1SX",
            WorkerId=workerId,
            IntegerValue=100,
            SendNotification=True
        )

        print(response)
