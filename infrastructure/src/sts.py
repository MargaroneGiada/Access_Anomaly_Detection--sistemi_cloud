import boto3

try:
    sts = boto3.client("sts")
except Exception as e:
    print(f"[STS] Error connecting to client: {e}")

account_id = sts.get_caller_identity()["Account"]

identity = sts.get_caller_identity()

