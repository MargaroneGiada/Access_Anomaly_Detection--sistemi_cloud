from src import s3
from src import apigateway as api
from src import dynamodb as db
# from src import cognito

s3.delete_bucket()
api.delete_api()
db.delete_users_table()

# cognito.delete_user_pool()