import json
import boto3
import os

BUCKET_NAME = os.getenv('BUCKET_NAME')

def getconfig(filepath: str = 'ShihTzu/config.json') -> dict:
    s3 = boto3.client('s3')
    try:
        data = s3.get_object(Bucket=BUCKET_NAME, Key=filepath)
        content = data['Body']
    except:
        print("The filepath does not exists!")
    print('Config loaded!')
    return json.load(content)

def saveconfig(config: dict, filepath: str = 'ShihTzu/config.json'):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Body=json.dumps(config,indent=2),Bucket=BUCKET_NAME, Key=filepath)
    except:
       print('Failed to save to S3!')
    print('Saved Sucessfully!')
