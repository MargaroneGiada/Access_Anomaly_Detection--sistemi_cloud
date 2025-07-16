import importlib
from src import s3
importlib.reload(s3)
from src import cognito
importlib.reload(cognito)

#S3
s3.delete_bucket()
s3.create_bucket()
s3.upload_website()

#Cognito
# cognito.delete_user_pool()
# cognito.create_user_pool()