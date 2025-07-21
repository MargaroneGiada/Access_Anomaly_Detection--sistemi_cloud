import boto3

try:
    ecr = boto3.client('ecr', region_name= 'us-east-1')
except Exception as e:
    print(f"[ECR] Error connecting to client: {e}")

def get_repo_uri():
    try:
        response = ecr.describe_repositories(repositoryNames=['signup'])
        repo_uri = response['repositories'][0]['repositoryUri']
        return repo_uri
    except Exception as e:
        print(f"[ECR] Error: {e}")

def create_repo():
    repo_name = 'signup'
    try:
        response = ecr.create_repository(repositoryName=repo_name)
        repository_uri = response['repository']['repositoryUri']
        print("[ECR] Created repository:", repository_uri)
    except Exception as e:
        print(f"[ECR] Errore while creating repository {repo_name}: {e}")

def delete_repo():
    repo_name = 'signup'
    try:
        ecr.delete_repository(repositoryName=repo_name, force=True)
        print("[ECR] Deleted repository")
    except Exception as e:
        print(f"[ECR] Errore while deleting repository {repo_name}: {e}")

