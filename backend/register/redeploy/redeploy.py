from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/redeploy', methods=['POST'])
def redeploy():
    os.system('aws s3 sync s3://aad-backend-hosting . --region us-east-1')
    os.system('docker stop $(docker ps -q)')
    os.system('docker rm $(docker ps -a -q)')
    os.system('docker build -t register .')
    os.system('docker run -d -p 5000:5000 register')
    return 'Redeploy triggered', 200

if __name__ == '__main__':
    app.run(port=9000)