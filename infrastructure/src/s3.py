import boto3
import os

try:
    s3 = boto3.client('s3')
    bucket_name = "aad-frontend-hosting"
    source_dir = "../frontend/aad-website/dist"
except Exception as e:
        print(f"[S3] Error connecting to client: {e}")

def empty_s3_bucket(bucket_name):
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket_name).objects.all().delete()
    except Exception as e:
        print(f"[S3] Error deleting objects: {e}")



def delete_bucket():
    try:
        empty_s3_bucket(bucket_name)
        response = s3.delete_bucket(
            Bucket=bucket_name
        )
        print(f"[S3] Deleting bucket: {bucket_name}")
        return response
    except Exception as e:
        print(f"[S3] Error deleting bucket: {e}")

    

def create_bucket():
    try:
        s3.create_bucket(
            Bucket=bucket_name
        )

        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': 'index.html'},
                'ErrorDocument': {'Key': 'index.html'}
            }
        )
        print(f"[S3] Created bucket: {bucket_name}")
    except Exception as e:
        print(f"[S3] Error creating bucket: {e}")


def upload_website():
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, source_dir)
            s3_key = relative_path.replace("\\", "/")

            print(f"[S3] Uploading {local_path} to s3://{bucket_name}/{s3_key}")
            s3.upload_file(local_path, bucket_name, s3_key)

