import boto3

try:
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
except Exception as e:
    print(f"[DynamoDB] Error connecting to client: {e}")

def create_users_table():
    try:
        dynamodb.create_table(
            TableName='Users',
            AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],
            KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print("[DynamoDB] Table 'Users' created.")
    except Exception as e:
        print(f'[DynamoDB] Error while creating user table: {e}')

def delete_users_table():
    try:
        dynamodb.delete_table(
            TableName='Users'
        )
        print("[DynamoDB] Table 'Users' deleted.")
    except Exception as e:
        print(f'[DynamoDB] Error while deleting user table: {e}')

