from src import s3
from src import cognito

s3.delete_bucket()

cognito.delete_user_pool()