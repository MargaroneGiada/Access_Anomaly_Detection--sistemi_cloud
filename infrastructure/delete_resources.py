from src import s3
from src import apigateway as api
from src import dynamodb as db
from src import ecr
from src import lambda_create as lamb
# from src import cognito

s3.delete_bucket()
api.delete_api()
db.delete_users_table()
ecr.delete_repo()
lamb.signup_remove_image()
lamb.delete_signup_lambda()
# cognito.delete_user_pool()