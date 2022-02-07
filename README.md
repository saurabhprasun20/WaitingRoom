# WaitingRoom

The waiting room has been designed to provide a waiting room option with Qualtrics Survey. The qualtrics client interacts with waiting room sever and closes the waiing
room as soon as minimum no of users are ready to take the survey.


## Server - 

1. server.py

The waiting room server is present in Flask Server package is used to create the waiting room. This is based on flask websocket. The server fetches the
required configuration from data.json. The server emits continue message as soon as there are minimum no of users are connected to the server.

## Qualtrics-client -
It contains the code to paste in the javascript section of qualtrics in order to communicate with the server. Modify the server address accordingly.

## MTurk Automation - 

1. automateHIT.py -> This file is used to create a HIT automatically on MTurk using boto3. It saves the HIT id into data.json file.
2. updateHIT.py -> This file is used to update a HIT. It fetches HIT id to update from data.json file.

## data.json - Contains the configuration for both waiting room server and Amazon Mturk automation.
### Fields
1. minimumNoOfUser - Declares the minimum no of user required to close the waiting room and continue with the survey.
2. hitId -  To update the same survey into MTurk, we need to maintain the HitId. This is updated automatically as soon as a new HIT is created on MTurk
3. question - Contains the link for qualtrics survey.
4. cycleChange - Do not change this variable. This is updated automatically based on state of waiting room server.
