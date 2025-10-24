import boto3
from src import config

cognito = boto3.client('cognito-idp', region_name='us-east-1')

def create_user_pool():
    try: 
        response = cognito.create_user_pool(
            PoolName='AccessAnomalyDetector',
            AutoVerifiedAttributes=['email'],
            UsernameAttributes=['email'],
            AccountRecoverySetting={
                'RecoveryMechanisms': [
                    {'Name': 'verified_email', 'Priority': 1}
                ]
            },
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': True,
                    'TemporaryPasswordValidityDays': 7
                }
            }, 
            DeletionProtection='INACTIVE'
        )
        pool_id = response['UserPool']['Id']
        config.USER_POOL_ID = pool_id
        print(f"[Cognito] Created User Pool: {pool_id}")
    except Exception as e:
        print(f"[Cognito] Error creating the user pool: {e}")
    return pool_id

def create_user_pool_client(user_pool_id):
    try:
        response = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName='AccessAnomalyDetectorAppClient',
            GenerateSecret=False,       
            ExplicitAuthFlows=[
                "ALLOW_USER_SRP_AUTH",
                "ALLOW_USER_PASSWORD_AUTH",
                "ALLOW_REFRESH_TOKEN_AUTH",
                "ALLOW_ADMIN_USER_PASSWORD_AUTH"
            ]
        )
        client_id = response['UserPoolClient']['ClientId']
        config.CLIENT_ID = client_id
        print(f"[Cognito] Created App Client: {client_id}")
    except Exception as e:
        print(f"[Cognito] Error creating the user pool client: {e}")
    return client_id

def delete_user_pool_client(id):
    try:
        list = cognito.list_user_pool_clients(UserPoolId=id, MaxResults=10);
        for userpoolclient in list["UserPoolClients"]:
            cognito.delete_user_pool_client(
                UserPoolId=userpoolclient["UserPoolId"],
                ClientId=userpoolclient["ClientId"]
            )
            print(f"[Cognito] Deleted App Client: {userpoolclient['ClientId']}")
        
    except Exception as e:
        print(f"[Cognito] Error deleting the user pool client: {e}")

def delete_all():
    try:
        list = cognito.list_user_pools(MaxResults=10);
        for userpool in list["UserPools"]:
            delete_user_pool_client(userpool["Id"])
            cognito.delete_user_pool(UserPoolId=userpool["Id"])
            print(f"[Cognito] Deleted User Pool: {userpool['Id']}")
        print(f"[Cognito] Delete completed")      
    except Exception as e:
        print(f"[Cognito] Error deleting user pool: {e}")

def signup(username, password, email, user_pool_id, client_id):
    try:
        cognito.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
            UserAttributes=[{'Name': 'email', 'Value': email}]
        )
        # conferma immediata (opzionale)
        cognito.admin_confirm_sign_up(
            UserPoolId=user_pool_id,
            Username=username
        )
        print(f"[Cognito] User {username} registered")  
    except Exception as e:
        print(f"[Cognito] Error during signup of {email}: {e}")

def login(email, password, user_pool_id, client_id):
    try:
        response = cognito.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        print(f"[Cognito] User with the email {email} is logged in")
    except Exception as e:
        print(f"[Cognito] User {email} could not log in: {e}")
    
    return {
        "idToken": response['AuthenticationResult']['IdToken'],
        "accessToken": response['AuthenticationResult']['AccessToken'],
        "refreshToken": response['AuthenticationResult']['RefreshToken']
    }


