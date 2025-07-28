import importlib
from src import s3
importlib.reload(s3)
from src import apigateway as api
importlib.reload(api)
from src import dynamodb as db
importlib.reload(db)
from src import ec2
from src import ecr
importlib.reload(ecr)
from src import lambda_signup as signup
importlib.reload(signup)
from src import sts
importlib.reload(sts)
from src import github_secrets

# from src import cognito
# importlib.reload(cognito)

# S3
s3.create_frontend_bucket()
s3.upload_website()
s3.create_backend_bucket()

#EC2
ec2.create_instance_signup()

#ECR
ecr.create_repo()

# API Gateway
api.create_api()
api.connect_lambda_to_api('SignupFunction')

# DynamoDB
db.create_users_table()

# #Lambda
# signup.signup_build_and_push_image()
# signup.create_signup_lambda()

# #Cognito
# cognito.create_user_pool()