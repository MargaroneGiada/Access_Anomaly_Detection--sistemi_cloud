import json
import boto3
import bcrypt
import time

try:
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
except Exception as e:
    print(f'[DynamoDB] Error while connecting to client: {e}')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body['email']
        password = body['password'].encode('utf-8')

        response = dynamodb.get_item(
            TableName='Users',
            Key={'email': {'S': email}}
        )
        if not ('Item' in response):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'User does not exists'})
            }
        

        if bcrypt.checkpw(password, response['Item']['password']['S'].encode('utf-8')):
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'User logged successfully'})
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Email or password does not match'})
            }

        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)})
        }
