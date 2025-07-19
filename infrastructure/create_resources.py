import importlib
from src import s3
importlib.reload(s3)
from src import apigateway as api
importlib.reload(api)
from src import dynamodb as db
importlib.reload(db)
# from src import cognito
# importlib.reload(cognito)

#S3
s3.create_bucket()
s3.upload_website()

#Cognito
# cognito.create_user_pool()

#API Gateway
api.create_api()

#DynamoDB
db.create_users_table()
