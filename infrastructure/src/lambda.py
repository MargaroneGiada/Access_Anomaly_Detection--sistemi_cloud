import os
import json
import boto3
from datetime import datetime
from src import config
from src import cognito

USER_POOL_ID = config.USER_POOL_ID
CLIENT_ID = config.CLIENT_ID

dynamo = boto3.client('dynamodb')

def log_attempt(email, success, ip='unknown', user_agent='unknown', action='unknown'):
    """Registra ogni tentativo in DynamoDB"""
    dynamo.put_item(
        TableName='AccessLogs',
        Item={
            'email': {'S': email},
            'timestamp': {'S': datetime.isoformat()},
            'ip': {'S': ip},
            'userAgent': {'S': user_agent},
            'success': {'BOOL': success},
            'action': {'S': action}
        }
    )

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action') 
        username = body.get('username')
        password = body.get('password')
        email = body.get('email', None)
        ip = event.get('requestContext', {}).get('http', {}).get('sourceIp', 'unknown')
        user_agent = event.get('headers', {}).get('user-agent', 'unknown')

        if action == 'signup':
            if not all([username, password, email]):
                return _response(400, {"error": "username, password e email richiesti"})
            return signup(username, password, email, ip, user_agent)

        elif action == 'login':
            if not all([username, password]):
                return _response(400, {"error": "username e password richiesti"})
            return login(username, password, ip, user_agent)

        else:
            return _response(400, {"error": "Azione non valida, deve essere 'signup' o 'login'"})

    except Exception as e:
        return _response(500, {"error": str(e)})

def signup(username, password, email, ip, user_agent):
    try:
        cognito.signup(username=username, password=password, email=email, user_pool_id=USER_POOL_ID, client_id=CLIENT_ID)

        log_attempt(username, True, ip, user_agent, action='signup')

        return _response(200, {"message": "Registrazione riuscita"})

    except cognito.exceptions.UsernameExistsException:
        log_attempt(username, False, ip, user_agent, action='signup')
        return _response(400, {"error": "Utente già esistente"})
    except Exception as e:
        log_attempt(username, False, ip, user_agent, action='signup')
        return _response(500, {"error": str(e)})

def login(email, password, ip, user_agent):
    try:
        response = cognito.login(
            user_pool_id=USER_POOL_ID,
            client_id=CLIENT_ID,
            email=email, 
            password=password
        )
        log_attempt(email, True, ip, user_agent, action='login')

        return _response(200, response)

    except cognito.exceptions.NotAuthorizedException:
        log_attempt(email, False, ip, user_agent, action='login')
        return _response(401, {"error": "Username o password errati"})
    except Exception as e:
        log_attempt(email, False, ip, user_agent, action='login')
        return _response(500, {"error": str(e)})

def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
