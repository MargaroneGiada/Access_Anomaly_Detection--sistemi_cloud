from src import s3
import importlib
importlib.reload(s3)

s3.delete_bucket()
s3.create_bucket()
s3.upload_website()