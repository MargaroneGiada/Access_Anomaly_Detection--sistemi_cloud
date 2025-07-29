from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/redeploy', methods=['POST'])
def redeploy():
    print("[Flask] Running redeploy...")
    os.system('cd /home/ec2-user/Access_Anomaly_Detection--sistemi_cloud')
    os.system('sudo git pull')
    os.system('sudo cp -r /home/ec2-user/.aws ./backend/register/.aws')
    os.system('cd backend/register')
    os.system('sudo docker stop $(sudo docker ps -q)')
    os.system('sudo docker rm $(sudo docker ps -a -q)')
    os.system('sudo docker build -t register .')
    os.system('sudo docker run -v ~/.aws:/root/.aws -d -p 5000:5000 register')
    print("[Flask] Redeploy finished")
    return 'Redeploy triggered', 200

if __name__ == '__main__':
    app.run(port=9000)