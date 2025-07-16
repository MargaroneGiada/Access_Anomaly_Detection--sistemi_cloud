import boto3

s3 = boto3.client('s3')
bucket_name = "aad-frontend-hosting"

def empty_s3_bucket(bucket_name):
    """Empties an S3 bucket of all its objects.

    Args:
        bucket_name (str): The name of the bucket to empty.
    """
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket_name).objects.all().delete()
    except Exception as e:
        print(f"Error deleting objects: {e}")



def delete_bucket():
    empty_s3_bucket(bucket_name)
    response = s3.delete_bucket(
        Bucket=bucket_name
    )
    print(f"Deleting bucket: {bucket_name}")

    return response

def create_bucket():
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

    print(f"Created bucket: {bucket_name}")


def upload_website():
    s3.upload_file('../frontend/aad-website/dist/index.html', bucket_name, 'index.html')
    s3.upload_file('../frontend/aad-website/dist/assets/index-i9tu7_r3.css', bucket_name, 'assets/index-i9tu7_r3.css')
    s3.upload_file('../frontend/aad-website/dist/assets/index-BtcBhzrb.js', bucket_name, 'assets/index-BtcBhzrb.js')