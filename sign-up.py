import boto3
import json

def lambda_handler(event, context):
    # Create a Cognito Identity Provider client
    client = boto3.client('cognito-idp')

    # Extract user data from event
    username = event.get('username')
    password = event.get('password')
    
    if not username or not password:
        return {
            'statusCode': 400,
            'body': json.dumps("Username and password are required")
        }

    try:
        # Perform the authentication
        response = client.admin_initiate_auth(
            UserPoolId='yyyyyyyyyyyyyyyyyy',  # Replace with your User Pool ID
            ClientId='xxxxxxxxxxxxxxxxxx',   # Replace with your App Client ID
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Authentication successful',
                'data': response['AuthenticationResult']
            })
        }
    except client.exceptions.NotAuthorizedException:
        return {
            'statusCode': 401,
            'body': json.dumps('The username or password is incorrect')
        }
    except client.exceptions.UserNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps('User does not exist')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }
