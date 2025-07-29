import boto3, os, time, base64
import json
from src import github_secrets as git

ec2 = boto3.resource('ec2', region_name='us-east-1')
client = boto3.client('ec2', region_name='us-east-1')

def create_or_get_security_group():
    try:
        response = client.describe_security_groups(GroupNames=['SecurityGroup'])
        return response['SecurityGroups'][0]['GroupId']
    except Exception as e:
        return create_security_group()

def create_security_group():
    group_name = 'SecurityGroup'
    description = 'Allow Flask on port 5000 and SSH'

    try:
        vpc_id = 'vpc-068e93bec3c58ce7c'

        response = ec2.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )
        security_group_id = response.id
        print(f"[EC2] Created Security Group {group_name} with ID: {security_group_id}")

        client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}] 
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}] 
                }
            ]
        )
        print(f"[EC2] Rules added to {group_name}")

        return security_group_id

    except Exception as e:
        print(f"[EC2] Error: {e}")
        return None


def create_instance_signup():

    with open("backend.zip", "rb") as f:
        encoded_zip = base64.b64encode(f.read()).decode("utf-8")

    sec_group_id = create_or_get_security_group()

    user_data_script = f"""#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

mkdir -p /home/ec2-user/.aws

cat > /home/ec2-user/.aws/credentials <<EOL
[default]
aws_access_key_id={git.SECRET_AWS_ACCESS_KEY_ID}
aws_secret_access_key={git.SECRET_AWS_SECRET_ACCESS_KEY}
aws_session_token={git.SECRET_AWS_SESSION_TOKEN}
EOL

cat > /home/ec2-user/.aws/config <<EOL
[default]
region = us-east-1
EOL

chown -R ec2-user:ec2-user /home/ec2-user/.aws
chmod 600 /home/ec2-user/.aws/credentials
chmod 644 /home/ec2-user/.aws/config

yum update -y
yum install -y docker git unzip
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

cd /home/ec2-user
git clone https://github.com/MargaroneGiada/Access_Anomaly_Detection--sistemi_cloud.git

sudo cp -r .aws Access_Anomaly_Detection--sistemi_cloud/backend/register/.aws

cd Access_Anomaly_Detection--sistemi_cloud/backend/register/

sudo docker build -t register .
sudo docker run -v ~/.aws:/root/.aws -d -p 5000:5000 register
"""


    instances = ec2.create_instances(
        ImageId='ami-08a6efd148b1f7504',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='SistemiCloudProject',
        SecurityGroupIds=[sec_group_id], 
        UserData=user_data_script,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'FlaskSignupInstance'}]
            }
        ]
    )

    print(f"[EC2] Created instance: {instances[0].id}")
    print("[EC2] Waiting for instance to be created...")

    instances[0].wait_until_running()
    instances[0].reload()

    with open('src/ec2.json') as f:
        json_data = json.load(f)  

    json_data.append({'id': instances[0].id, 'ip': instances[0].public_ip_address})

    with open("./src/ec2.json", "w", encoding='utf-8') as f:
        json.dump(json_data,f,ensure_ascii=False, indent=2)

    return instances[0].id

def terminate_all_instances():
    ec2_file_path = './src/ec2.json'
    if not os.path.exists(ec2_file_path):
        print("[EC2] No instances to terminate.")
        return

    with open(ec2_file_path) as f:
        json_data = json.load(f)

    for instance in json_data:
        instance_id = instance['id']
        print(f"[EC2] Terminating instance: {instance_id}")
        try:
            instance = ec2.Instance(instance_id)
            instance.terminate()
        except Exception as e:
            print(f"[EC2] Error terminating {instance_id}: {e}")
    
    time.sleep(15)

    try:
        client.delete_security_group(
            GroupName='SecurityGroup'
        )   
    except Exception as e:
        print(f"[EC2] Error deleting security group: {e}")
    
    with open(ec2_file_path, 'w') as f:
        f.write('[]')

    print("[EC2] All instances terminated and security group removed")
