import boto3, mimetypes
import os
import json

try:
    s3 = boto3.client('s3')
    bucket_name = "aad-frontend-hosting"
    source_dir = "../frontend/aad-website/dist"
    bucket_name_backend = "aad-backend-hosting"
    source_dir_backend = "../backend/register"
except Exception as e:
        print(f"[S3] Error connecting to client: {e}")

def empty_s3_bucket(bucket_name):
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket_name).objects.all().delete()
    except Exception as e:
        print(f"[S3] Error deleting objects: {e}")


def delete_frontend_bucket():
    try:
        empty_s3_bucket(bucket_name)
        response = s3.delete_bucket(
            Bucket=bucket_name
        )
        print(f"[S3] Deleted bucket: {bucket_name}")
        return response
    except Exception as e:
        print(f"[S3] Error deleting bucket: {e}")

def create_frontend_bucket():
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

        s3.delete_public_access_block(
            Bucket=bucket_name
        )

        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )

        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )

        print(f"[S3] Created bucket: {bucket_name}")
    except Exception as e:
        print(f"[S3] Error creating bucket: {e}")


def upload_website():
    for root, _, files in os.walk(source_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, source_dir)
            s3_key = relative_path.replace("\\", "/")

            mime_type, _ = mimetypes.guess_type(local_path)
            if not mime_type:
                mime_type = "binary/octet-stream"

            print(f"[S3] Uploading {local_path} to s3://{bucket_name}/{s3_key} with content-type {mime_type}")
            try:
                s3.upload_file(
                    Filename=local_path,
                    Bucket=bucket_name,
                    Key=s3_key,
                    ExtraArgs={'ContentType': mime_type}
                )
            except Exception as e:
                print(f"[S3] Error uploading {s3_key}: {e}")

def create_backend_bucket():
    try:
        s3.create_bucket(
            Bucket=bucket_name_backend
        )

        s3.delete_public_access_block(
            Bucket=bucket_name_backend
        )

        s3.put_public_access_block(
            Bucket=bucket_name_backend,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )

        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name_backend}/*"
                }
            ]
        }

        s3.put_bucket_policy(
            Bucket=bucket_name_backend,
            Policy=json.dumps(bucket_policy)
        )

        print(f"[S3] Created bucket: {bucket_name_backend}")
    except Exception as e:
        print(f"[S3] Error creating bucket: {e}")

    for root, _, files in os.walk(source_dir_backend):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, source_dir_backend)
            s3_key = relative_path.replace("\\", "/")

            mime_type, _ = mimetypes.guess_type(local_path)
            if not mime_type:
                mime_type = "binary/octet-stream"

            print(f"[S3] Uploading {local_path} to s3://{bucket_name_backend}/{s3_key} with content-type {mime_type}")
            try:
                s3.upload_file(
                    Filename=local_path,
                    Bucket=bucket_name_backend,
                    Key=s3_key,
                    ExtraArgs={'ContentType': mime_type}
                )
            except Exception as e:
                print(f"[S3] Error uploading {s3_key}: {e}")


def delete_backend_bucket():
    try:
        empty_s3_bucket(bucket_name_backend)
        response = s3.delete_bucket(
            Bucket=bucket_name_backend
        )
        print(f"[S3] Deleted bucket: {bucket_name_backend}")
        return response
    except Exception as e:
        print(f"[S3] Error deleting bucket: {e}")