import boto3
import time

try:
    cloudfront = boto3.client('cloudfront')
except Exception as e:
        print(f"[CloudFront] Error connecting to client: {e}")

def create_oac():
    try:
        response = cloudfront.create_origin_access_control(
            OriginAccessControlConfig={
                "Name": "aad-oac",
                "Description": "OAC per distribuzione AAD",
                "SigningProtocol": "sigv4",
                "SigningBehavior": "always",
                "OriginAccessControlOriginType": "s3"
            }
        )
        print(f"[CloudFront] Created origin access control: {response["OriginAccessControl"]["Id"]}")
        return response["OriginAccessControl"]["Id"]
    except Exception as e:
        print(f"[CloudFront] Error creating origin access control: {e}")

def delete_oac():
        list = cloudfront.list_origin_access_controls()
        if list["OriginAccessControlList"]["Quantity"]>0:
            for oac_id in list["OriginAccessControlList"]["Items"]:
                resp = cloudfront.get_origin_access_control(Id=oac_id["Id"])
                etag = resp["ETag"]
                try:
                    cloudfront.delete_origin_access_control(
                        Id=oac_id["Id"],
                        IfMatch=etag
                    )
                    print(f"[CloudFront] Deleted origin access control: {oac_id["Id"]}")
                except Exception as e:
                    print(f"[CloudFront] Error deleting origin access control {oac_id}: {e}")

def create_distribution(oac_id):
    """
    Creates a CloudFront distribution with the Origin Access Control given id
    Returns DomainName, ID and ARN
    """
    try:
        distribution_config = {
            "CallerReference": "aad-distribution",
            "Comment": "Distribuzione per hosting frontend",
            "Enabled": True,
            "Origins": {
                "Quantity": 1,
                "Items": [
                    {
                        "Id": "aad-s3-origin",
                        "DomainName": "aad-frontend-hosting.s3.us-east-1.amazonaws.com",
                        "S3OriginConfig": {
                            "OriginAccessIdentity": ""
                        },
                        "OriginAccessControlId": oac_id
                    }
                ]
            },
            "DefaultCacheBehavior": {
                "TargetOriginId": "aad-s3-origin",
                "ViewerProtocolPolicy": "redirect-to-https",
                "AllowedMethods": {
                    "Quantity": 2,
                    "Items": ["GET", "HEAD"]
                },
                "Compress": True,
                "ForwardedValues": {
                    "QueryString": False,
                    "Cookies": {"Forward": "none"}
                },
                "DefaultTTL": 3600,
                "MaxTTL": 86400,
                "MinTTL": 0
            },
            "DefaultRootObject": "index.html"
        }

        response = cloudfront.create_distribution(DistributionConfig=distribution_config)

        distribution_id = response["Distribution"]["Id"]
        distribution_domain = response["Distribution"]["DomainName"]

        print("[CloudFront] Distribution ID:", distribution_id)
        print("[CloudFront] Distribution Domain:", distribution_domain)
        wait_until_deployed(distribution_id)
        print(f"[CloudFront] Created distribution {distribution_id}: {distribution_domain}")
        return response["Distribution"]["DomainName"], response["Distribution"]["Id"], response["Distribution"]["ARN"]
    except Exception as e:
        print(f"[CloudFront] Error creating distribution: {e}")

def delete_distribution():
    list = cloudfront.list_distributions()
    if list["DistributionList"]["Quantity"] > 0:
        for distribution_id in list["DistributionList"]["Items"]:
            etag = disable_distribution(distribution_id["Id"])
            try:
                cloudfront.delete_distribution(
                    Id=distribution_id["Id"],
                    IfMatch=etag
                )
                print(f"[CloudFront] Deleted distribution: {distribution_id["Id"]}")
            except Exception as e:
                print(f"[CloudFront] Error deleting distribution {distribution_id}: {e}")


def disable_distribution(distribution_id):
    response = cloudfront.get_distribution_config(Id=distribution_id)
    etag = response["ETag"]
    config = response["DistributionConfig"]

    config["Enabled"] = False

    result = cloudfront.update_distribution(
        Id=distribution_id,
        IfMatch=etag,
        DistributionConfig=config
    )
    wait_until_deployed(distribution_id)
    print(f"[CloudFront] Distribuzione {distribution_id} disabilitata.")
    response = cloudfront.get_distribution_config(Id=distribution_id)
    etag = response["ETag"]
    return etag

def wait_until_deployed(distribution_id, delay=30):
    while True:
        resp = cloudfront.get_distribution(Id=distribution_id)
        status = resp["Distribution"]["Status"]
        print(f"[CloudFront] Distribuzione {distribution_id} status: {status}")
        if status == "Deployed":
            break
        time.sleep(delay)