from flask import Flask, request, jsonify
import json, bcrypt, os
import boto3
import time

app = Flask(__name__)

try:
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
except Exception as e:
    print(f'[DynamoDB] Error while connecting to client: {e}')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password').encode('utf-8')


        if not username or not email or not password:
            return jsonify({'error': 'Missing fields'}), 400

        response = dynamodb.get_item(
            TableName='Users',
            Key={'email': {'S': email}}
        )

        print(username, email, password)

        if 'Item' in response:
            return jsonify({'message': 'User already exists'}), 400

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)

        dynamodb.put_item(
            TableName='Users',
            Item={
                'email': {'S': email},
                'password': {'S': hashed.decode('utf-8')},
                'created_at': {'S': str(int(time.time()))},
                'username': {'S': username}
            }
        )

        print(username, email, password)

        return jsonify({'message': 'User created successfully! :)'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password').encode('utf-8')


        if not email or not password:
            return jsonify({'error': 'Missing fields'}), 400

        response = dynamodb.get_item(
            TableName='Users',
            Key={'email': {'S': email}}
        )


        if not 'Item' in response:
            return jsonify({'message': 'Email or password does not match'}), 400

        if bcrypt.checkpw(password, response['Item']['password']['S'].encode('utf-8')):
            return jsonify({'message': 'User logged successfully'}), 200
        else:
            return jsonify({'message': 'Email or password does not match'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/redeploy', methods=['POST'])
# def redeploy():
#     os.system('cd /home/ec2-user/Access_Anomaly_Detection--sistemi_cloud')
#     os.system('git pull')
#     os.system('sudo cp -r /home/ec2-user/.aws /backend/register/.aws')
#     os.system('cd ./backend/register')
#     os.system('sudo docker stop $(sudo docker ps -q)')
#     os.system('sudo docker rm $(sudo docker ps -a -q)')
#     os.system('sudo docker build -t register .')
#     os.system('sudo docker run -v ~/.aws:/root/.aws -d -p 5000:5000 register')
#     return 'Redeploy triggered', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
