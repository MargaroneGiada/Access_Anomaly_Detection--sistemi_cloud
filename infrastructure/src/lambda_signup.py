import boto3, subprocess
from src import sts
from src import ecr

region = 'us-east-1'
image_name = 'signup'
account_id = sts.account_id 


def signup_build_and_push_image():
    repo_uri = ecr.get_repo_uri()

    #creazione immagine docker
    subprocess.run(['docker', 'build', '-t', image_name, '../backend/signup'], check=True)

    #push immagine su ecr
    subprocess.run([
        'docker', 'tag', f'{image_name}:latest', f'{repo_uri}:latest'
    ], check=True)
    password = subprocess.check_output(
        ['aws', 'ecr', 'get-login-password', '--region', 'us-east-1'],
        text=True
    )
    subprocess.run(
        ['docker', 'login', '--username', 'AWS', '--password-stdin', repo_uri],
        input=password,
        text=True,
        check=True
    )
    subprocess.run(['docker', 'push', f'{repo_uri}:latest'], check=True)
    print("[Docker] Built and pushed 'signup' image")


def signup_remove_image():
    repo_uri = ecr.get_repo_uri()
    # subprocess.run(['docker', 'rm', '-f', 'signup'], check=False)
    subprocess.run(['docker', 'rmi', f'{repo_uri}:latest'], check=True)
    subprocess.run(['docker', 'rmi', 'signup:latest'], check=False)
    print("[Docker] Removed 'signup' container and images")



def create_signup_lambda():
    lambda_client = boto3.client('lambda', region_name=region)
    role_name = "LabRole"
    repo_uri = ecr.get_repo_uri()
    try:
        response = lambda_client.create_function(
            FunctionName='SignupFunction',
            Role=f'arn:aws:iam::{account_id}:role/{role_name}',
            PackageType='Image',
            Code={'ImageUri': f'{repo_uri}:latest'},
            Timeout=15,
            MemorySize=128,
            Publish=True
        )
        print("[Lambda] Created lambda function 'signup':", response['FunctionArn'])
    except Exception as e:
        print(f'[Lambda] Error: {e}')

def delete_signup_lambda():

    lambda_client = boto3.client('lambda', region_name=region)
    try:
        response = lambda_client.delete_function(
            FunctionName='SignupFunction'
        )
        print("[Lambda] Deleted lambda function 'signup':", response['FunctionArn'])
    except Exception as e:
        print(f'[Lambda] Error: {e}')

