import boto3

try:
    apigateway = boto3.client('apigatewayv2', 'us-east-1')
except Exception as e:
    print(f"[API Gateway] Error connecting to client: {e}")

def create_api():
    try:
        response = apigateway.create_api(
            Name='AccessAnomalyDetector-API',
            ProtocolType='HTTP'
        )

        api_id = response['ApiId']

        print(f"API created with ID: {api_id}")
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
                    return None
                except Exception as e:
                    print(f"[API Gateway] Error while deleting api: {e}")
                    return None
        print(f"[API Gateway] API with {api_name} name not found.")
    except Exception as e:
        print(f"Error fetching APIs: {e}")
        return None

