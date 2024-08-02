import json
import boto3
from datetime import datetime

def lambda_handler(event,context):
    ec2_client = boto3.client('ec2')
    
    # Get the instance ID from the event
    #instance_id = event['instance_id']
    instance_id = 'i-0096708f2e52a5625'
    
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Tags to apply
    tags = [
        {'Key': 'LaunchDate', 'Value': current_date},
        {'Key': 'CustomTag', 'Value': 'YourValue'}  # Replace 'YourValue' with your custom value
    ]
    
    # Tag the instance
    response = ec2_client.create_tags(
        Resources=[instance_id],
        Tags=tags
    )
    
    print(response)
    
    print(f"Successfully tagged instance {instance_id} with tags: {tags}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Tagging successful!')
    }
    


