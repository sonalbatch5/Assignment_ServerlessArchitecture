**Assignment 3: Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3**

Objective: Learn to automate the tagging of EC2 instances as soon as they are launched, ensuring better resource tracking and management.

Task: Automatically tag any newly launched EC2 instance with the current date and a custom tag.

Instructions:

1. EC2 Setup:

   - Ensure you have the capability to launch EC2 instances.

2. Lambda IAM Role:

   - In the IAM dashboard, create a new role for Lambda.

   - Attach the `AmazonEC2FullAccess` policy to this role.

3. Lambda Function:

   - Navigate to the Lambda dashboard and create a new function.

   - Choose Python 3.x as the runtime.

   - Assign the IAM role created in the previous step.

   - Write the Boto3 Python script to:

     1. Initialize a boto3 EC2 client.

     2. Retrieve the instance ID from the event.

     3. Tag the new instance with the current date and another tag of your choice.

     4. Print a confirmation message for logging purposes.

4. CloudWatch Events:

   - Set up a CloudWatch Event Rule to trigger the EC2 instance launch event.

   - Attach the Lambda function as the target.

5. Testing:

   - Launch a new EC2 instance.

   - After a short delay, confirm that the instance is automatically tagged as specified.
