
import json
import boto3
import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    # Extract URL from the event
    url = event['url']
    
    # Scrape the webpage and extract data
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    # extract all the data you wish to collect from the webpage
    
    # Upload data to S3 bucket
    s3 = boto3.resource('s3')
    bucket_name = 'your-bucket-name'
    key = event['key']
    s3.Object(bucket_name, key).put(Body=json.dumps(data))
    
    # Return successful status
    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully uploaded to S3')
    }
