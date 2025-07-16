import boto3

cognito = boto3.client('cognito-idp', 'us-east-1')

def delete_user_pool():
    
    response = cognito.list_user_pools(MaxResults=5)
    user_pools = response.get("UserPools", [])

    for pool in user_pools:
        pool_id = pool["Id"]
        print(f"Deleting App Clients in user pool: {pool_id}")
        
        clients_response = cognito.list_user_pool_clients(
            UserPoolId=pool_id,
            MaxResults=5
        )
        for client_desc in clients_response.get("UserPoolClients", []):
            client_id = client_desc["ClientId"]
            print(f"  Deleting App Client: {client_id}")
            cognito.delete_user_pool_client(
                UserPoolId=pool_id,
                ClientId=client_id
            )
        
        print(f"Deleting user pool: {pool_id}")
        cognito.delete_user_pool(UserPoolId=pool_id)


def create_user_pool():
    user_pool = cognito.create_user_pool(
        PoolName="aad-user-pool",
        AutoVerifiedAttributes=["email"],  
        UsernameAttributes=["email"],      
        MfaConfiguration="OFF"             
    )
    user_pool_id = user_pool["UserPool"]["Id"]

    app_client = cognito.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName="aad-user-pool-client",
        GenerateSecret=False,  
        AllowedOAuthFlows=['code'],  
        AllowedOAuthScopes=[
            'openid',  
            'email',
            'profile'
        ],
        AllowedOAuthFlowsUserPoolClient=True,
        CallbackURLs=["http://localhost"],  
        LogoutURLs=["http://localhost"],
        SupportedIdentityProviders=['COGNITO'],
    )

    print(f"Created user pool 'aad-user-pool', id: {user_pool_id}")
    return user_pool_id, app_client

# delete_user_pool()
create_user_pool()
