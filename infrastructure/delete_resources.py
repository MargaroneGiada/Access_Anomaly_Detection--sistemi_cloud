from src import s3
from src import apigateway as api
from src import dynamodb as db
from src import ecr
from src import lambda_signup as lamb
from src import ec2
# from src import cognito

s3.delete_frontend_bucket()
s3.delete_backend_bucket()
api.delete_api()
db.delete_users_table()
ecr.delete_repo()
ec2.terminate_all_instances()
# lamb.signup_remove_image()
# lamb.delete_signup_lambda()

# cognito.delete_user_pool()