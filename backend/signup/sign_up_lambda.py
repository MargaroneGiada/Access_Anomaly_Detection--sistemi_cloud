import json
import boto3
import bcrypt
import time

# TODO
# runnare docker buil e docker run e testare se ora funziona
# versione pushata non funzionante

dynamodb = boto3.client('dynamodb', region_nam='us-east-1')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body['email']
        password = body['password'].encode('utf-8')

        response = dynamodb.get_item(
            TableName='Users',
            Key={'email': {'S': email}}
        )
        if 'Item' in response:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'User already exists'})
            }

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        dynamodb.put_item(
            TableName='Users',
            Item={
                'email': {'S': email},
                'password': {'S': hashed.decode('utf-8')},
                'created_at': {'S': str(int(time.time()))}
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)})
        }
