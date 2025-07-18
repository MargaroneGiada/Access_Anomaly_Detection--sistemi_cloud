import boto3

try:
    s3 = boto3.client('s3')
    bucket_name = "aad-frontend-hosting"
except Exception as e:
        print(f"[S3] Error connecting to client: {e}")

def empty_s3_bucket(bucket_name):
    """Empties an S3 bucket of all its objects.

    Args:
        bucket_name (str): The name of the bucket to empty.
    """
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
    s3.upload_file('../frontend/aad-website/dist/index.html', bucket_name, 'index.html')
    s3.upload_file('../frontend/aad-website/dist/assets/index-i9tu7_r3.css', bucket_name, 'assets/index-i9tu7_r3.css')
    s3.upload_file('../frontend/aad-website/dist/assets/index-BtcBhzrb.js', bucket_name, 'assets/index-BtcBhzrb.js')