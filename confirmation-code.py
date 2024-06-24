import boto3
import json


def lambda_handler(event, context):
    # Create a Cognito Identity Provider client
    client = boto3.client('cognito-idp')

    # Extract confirmation code and username from the event
    username = event.get('username')  # The username must be the one used during the signup
    confirmation_code = event.get('confirmationCode')
    
    if not username or not confirmation_code:
        return {
            'statusCode': 400,
            'body': json.dumps("Username and confirmation code are required")
        }

    try:
        # Attempt to confirm the user's registration
        response = client.confirm_sign_up(
            ClientId='xxxxxxxxxxxxxxxxxx',  # Replace with your actual App Client ID
            Username=username,
            ConfirmationCode=confirmation_code,
            ForceAliasCreation=False
        )
        return {
            'statusCode': 200,
            'body': json.dumps('User confirmation successful')
        }
    except client.exceptions.UserNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps('User not found')
        }
    except client.exceptions.CodeMismatchException:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid confirmation code')
        }
    except client.exceptions.ExpiredCodeException:
        return {
            'statusCode': 410,
            'body': json.dumps('Confirmation code expired')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }