import boto3


def stop_instance(instance_id):
    # Create an EC2 client
    ec2 = boto3.client('ec2')

    # Stop the instance
    response = ec2.stop_instances(InstanceIds=[instance_id])

    http_code = response['ResponseMetadata']['HTTPStatusCode']

        # Check the response
    for instance in response['StoppingInstances']:
        if instance['InstanceId'] == instance_id:
            current_state = instance['CurrentState']['Name']
            previous_state = instance['PreviousState']['Name']
            print(f"Instance {instance_id} state changed from {previous_state} to {current_state}")

            if http_code == 200 and (current_state == 'stopping' or current_state == 'stopped'):
                return True, http_code
            else:
                return False, http_code
            
def start_instance(instance_id):
    # Create an EC2 client
    ec2 = boto3.client('ec2')

    # Stop the instance
    response = ec2.start_instances(InstanceIds=[instance_id])

    http_code = response['ResponseMetadata']['HTTPStatusCode']

    print(response)

        # Check the response
    for instance in response['StartingInstances']:
        if instance['InstanceId'] == instance_id:
            current_state = instance['CurrentState']['Name']
            previous_state = instance['PreviousState']['Name']
            print(f"Instance {instance_id} state changed from {previous_state} to {current_state}")

            if http_code == 200 and (current_state == 'running'):
                return True, http_code
            else:
                return False, http_code

def lambda_handler():
    ec2 = boto3.client('ec2')
    
    # Describe instances with the 'Auto-Stop' tag
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            }
        ]
    )

    #print(response)
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            #if instance_state != "terminated" and instance_state != "stopped":
            print(f"Starting instance with Instance ID: {instance_id}, State: {instance_state}")
            response = start_instance(instance_id)
            print(response)

def main():
    print("Hello from main function!")
    lambda_handler()

if __name__ == "__main__":
    main()