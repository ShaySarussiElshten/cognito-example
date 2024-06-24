import boto3
import json


def lambda_handler(event, context):
    # Create a Cognito Identity Provider client
    client = boto3.client('cognito-idp')

    # Extract user data from event
    # Assuming 'username' in the event is the email address
    email = event.get('username')  # Make sure 'username' is passed in the event and is an email
    password = event.get('password')
    
    
    if not email or not password:
        return {
            'statusCode': 400,
            'body': json.dumps("Username and password are required")
        }

    try:
        # Call Cognito to create a new user
        response = client.sign_up(
            ClientId='xxxxxxxxxxxxxxxxxxxx',  # Replace with your actual App Client ID
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                # Add other attributes here if necessary
            ]
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Registration successful')
        }
    except client.exceptions.UsernameExistsException:
        return {
            'statusCode': 409,
            'body': json.dumps('Username already exists')
        }
    except client.exceptions.InvalidParameterException as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }

