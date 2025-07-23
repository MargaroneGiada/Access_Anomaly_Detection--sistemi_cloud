import importlib
from src import s3
importlib.reload(s3)
from src import apigateway as api
importlib.reload(api)
from src import dynamodb as db
importlib.reload(db)
from src import ecr
importlib.reload(ecr)
from src import lambda_create as lamb
importlib.reload(lamb)
from src import sts
importlib.reload(sts)
# from src import cognito
# importlib.reload(cognito)

# # S3
# s3.create_bucket()
# s3.upload_website()

# #ECR
# ecr.create_repo()

# # API Gateway
# api.create_api()

api.connect_lambda_to_api('SignupFunction')

# # DynamoDB
# db.create_users_table()

# #Lambda
# lamb.signup_build_and_push_image()
# lamb.create_signup_lambda()

# #Cognito
# cognito.create_user_pool()