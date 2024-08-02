import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler():
    s3 = boto3.client('s3')
    bucket_name = 'sonal-bucket'
    days_old = 30  # Temporary adjustment for testing
    delete_time = datetime.now(timezone.utc) - timedelta(days=days_old)
    
    # List objects in the specified bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    print(response)
    
    if 'Contents' not in response:
        print("Bucket is empty.")
        return {
            'statusCode': 200,
            'body': "Bucket is empty."
        }
    
    delete_keys = []
    for obj in response['Contents']:
        print(f"Object: {obj['Key']}, LastModified: {obj['LastModified']}")
        if obj['LastModified'] < delete_time:
            delete_keys.append({'Key': obj['Key']})
            print(f"Object {obj['Key']} is older than 30 days and will be deleted")
    
    if delete_keys:
        print(f"Deleting objects: {delete_keys}")
        s3.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_keys})
        deleted_objects = [key['Key'] for key in delete_keys]
        print(f"Deleted objects: {deleted_objects}")
    else:
        print("No objects older than 30 days found.")
    
    return {
        'statusCode': 200,
        'body': f"Deleted objects: {delete_keys}"
    }


def main():
    print("Hello from main function!")
    lambda_handler()

if __name__ == "__main__":
    main()