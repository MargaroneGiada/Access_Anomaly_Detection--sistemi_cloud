import boto3
from src import sts
import json

try:
    apigateway = boto3.client('apigatewayv2', 'us-east-1')
    json_list = []
    json_string = {}
    lambda_client = boto3.client('lambda', region_name='us-east-1')

except Exception as e:
    print(f"[API Gateway] Error connecting to client: {e}")

def create_api():
    try:
        response = apigateway.create_api(
            Name='AccessAnomalyDetector-API',
            ProtocolType='HTTP'
        )

        api_id = response['ApiId']

        json_string = {
            'api_id': api_id
        }
        json_list.append(json_string)

        with open("./src/apigateway.json", "w", encoding='utf-8') as f:
            json.dump(json_list,f,ensure_ascii=False, indent=2)

        print(f"[API Gateway] created with ID: {api_id}")
        return api_id
    except Exception as e:
        print(f"[API Gateway] Error crating API: {e}")

def delete_api():
    try:
        apis = apigateway.get_apis()['Items']
        api_name = 'AccessAnomalyDetector-API'
        for api in apis:
            if api['Name'] == api_name:
                id = api['ApiId']
                try:
                    apigateway.delete_api(ApiId=id)
                    print(f"[API Gateway] Deleted api: {id}")
                    return None
                except Exception as e:
                    print(f"[API Gateway] Error while deleting api: {e}")
                    return None
        print(f"[API Gateway] API with {api_name} name not found.")
    except Exception as e:
        print(f"[API Gateway] Error fetching APIs: {e}")
        return None


def connect_lambda_to_api(lambda_name):
    with open('apigateway.json') as f:
        json_data = json.load(f)    
    api_id = json_data['api_id']

    try:
        lambda_info = lambda_client.get_function(FunctionName=lambda_name)
        lambda_arn = lambda_info['Configuration']['FunctionArn']
    except Exception as e:
        print(f"[Lambda] Error retrieving function ARN: {e}")
        return
    
    try:
        integration = apigateway.create_integration(
            ApiId=api_id,
            IntegrationType='AWS_PROXY',
            IntegrationUri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations',
            PayloadFormatVersion='2.0'
        )
        integration_id = integration['IntegrationId']
    except Exception as e:
        print(f"[API Gateway] Error creating integration: {e}")
        return
    
    try:
        route = apigateway.create_route(
            ApiId=api_id,
            RouteKey='POST /signup',
            Target=f'integrations/{integration_id}'
        )
    except Exception as e:
        print(f"[API Gateway] Error creating route: {e}")
        return
    
    try:
        # 4. Grant API Gateway permission to invoke Lambda
        lambda_client.add_permission(
            FunctionName=lambda_name,
            StatementId=f'{lambda_name}-invoke-permission',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-1:{sts.account_id}:{api_id}/*/POST/signup'
        )
    except lambda_client.exceptions.ResourceConflictException:
        print(f"[Lambda] Permission already exists for {lambda_name}")
    except Exception as e:
        print(f"[Lambda] Error granting API Gateway permission to invoke Lambda: {e}")
        return

    apigateway.create_stage(
        ApiId=api_id,
        StageName='prod',
        AutoDeploy=True
    )

    endpoint = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/signup"
    print(f"[API Gateway] Lambda connected to route. Endpoint: {endpoint}")
    return endpoint