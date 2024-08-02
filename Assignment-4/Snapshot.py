import boto3
import datetime
import json

ec2_client = boto3.client('ec2')

# Initialize boto3 client for EC2
ec2_client = boto3.client('ec2')

# Function to create a snapshot of the volume of a given instance
def create_snapshot(instance_id):
    # Get all volumes attached to the instance
    volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])
    
    # Iterate through each volume and create a snapshot
    for volume in volumes['Volumes']:
        volume_id = volume['VolumeId']
        snapshot = ec2_client.create_snapshot(VolumeId=volume_id, Description=f'Snapshot of {instance_id} - {volume_id}')
        print(f'Created snapshot: {snapshot["SnapshotId"]} for volume: {volume_id}')

# Function to list all snapshots of the given instance
def list_snapshots(instance_id):
    snapshots = ec2_client.describe_snapshots(Filters=[{'Name': 'description', 'Values': [f'Snapshot of {instance_id} - *']}])
    for snapshot in snapshots['Snapshots']:
        print(f'Snapshot ID: {snapshot["SnapshotId"]}, Description: {snapshot["Description"]}, Start Time: {snapshot["StartTime"]}')

# Function to delete snapshots of a specific instance older than 10 days
def delete_old_snapshots(instance_id):
    snapshots = ec2_client.describe_snapshots(Filters=[{'Name': 'description', 'Values': [f'Snapshot of {instance_id} - *']}])
    now = datetime.datetime.utcnow()
    # time_diff = now - datetime.timedelta(days=30)
    time_diff = now - datetime.timedelta(minutes=1)

    
    for snapshot in snapshots['Snapshots']:
        start_time = snapshot['StartTime'].replace(tzinfo=None)
        if start_time < time_diff:
            ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            print(f'Deleted snapshot: {snapshot["SnapshotId"]}')

def lambda_handler(event, context):
    instance_id = 'i-0096708f2e52a5625'  # Replace with your EC2 instance ID
    create_snapshot(instance_id)
    list_snapshots(instance_id)
    delete_old_snapshots(instance_id)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    instance_id = 'i-0096708f2e52a5625'  # Replace with your EC2 instance ID
    create_snapshot(instance_id)
    list_snapshots(instance_id)
    delete_old_snapshots(instance_id)
