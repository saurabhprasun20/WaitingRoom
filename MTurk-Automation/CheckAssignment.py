import boto3, csv, os, shutil, datetime

region_name = 'us-east-1'

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
)

sibB = os.path.join(os.path.dirname(__file__), '..', 'data/Pending')
for filename in os.listdir(sibB):
    if filename == 'assignment_status.csv':

        with open(os.path.join(sibB, "assignment_status.csv"), 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row['assignmentId'])
                print(row['status'])
                requester_feedback = ''
                override_rejection = False

                if row['requesterFeedback'] != '':
                    requester_feedback = row['requesterFeedback']
                    print(requester_feedback)

                if row['overrideRejection'] == 'True':
                    override_rejection = True
                    print(override_rejection)

                if row['status'] == 'True' or row['status'] == '1':
                    response = client.approve_assignment(
                        AssignmentId=row['assignmentId'],
                        RequesterFeedback=requester_feedback,
                        OverrideRejection=override_rejection
                    )
                    approved_file_path = os.path.join(os.path.dirname(__file__), '..', 'data/Approved')
                    for approved_file in os.listdir(approved_file_path):
                        if approved_file == 'assignment_approved.csv':
                            with open(os.path.join(approved_file_path, approved_file), 'a',
                                      newline='') as approved_csv_file:
                                writer = csv.writer(approved_csv_file)
                                writer.writerow([row['assignmentId'], row['status']])

                if row['status'] == 'False' or row['status'] == '0':
                    response = client.reject_assignment(
                        AssignmentId=row['assignmentId'],
                        RequesterFeedback=requester_feedback
                    )

                    rejected_file_path = os.path.join(os.path.dirname(__file__), '..', 'data/Rejected')
                    for rejected_file in os.listdir(rejected_file_path):
                        if rejected_file == 'assignment_rejected.csv':
                            with open(os.path.join(rejected_file_path, rejected_file), 'a',
                                      newline='') as rejected_csv_file:
                                writer = csv.writer(rejected_csv_file)
                                writer.writerow([row['assignmentId'], row['status']])
        os.rename(os.path.join(sibB, "assignment_status.csv"), os.path.join(sibB, "assignment_status_processed-"+str(datetime.datetime.now())+".csv"))