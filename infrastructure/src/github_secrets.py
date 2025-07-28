import requests
from base64 import b64encode
import os
from nacl import encoding, public

def get_aws_credential_value(key="aws_access_key_id"):
    path = os.path.expanduser("~/.aws/credentials")
    with open(path, "r") as f:
        dentro = False
        for line in f:
            if line.strip() == f"[{'default'}]":
                dentro = True
                continue
            if dentro:
                if line.startswith("[") and "]" in line:
                    break 
                if line.strip().startswith(key):
                    return line.split("=", 1)[1].strip()
    return None

OWNER = "MargaroneGiada"
REPO = "Access_Anomaly_Detection--sistemi_cloud"
TOKEN = "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"
AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
AWS_SESSION_TOKEN = "AWS_SESSION_TOKEN"
SECRET_AWS_ACCESS_KEY_ID = get_aws_credential_value('aws_access_key_id')
SECRET_AWS_SECRET_ACCESS_KEY = get_aws_credential_value('aws_secret_access_key')
SECRET_AWS_SESSION_TOKEN = get_aws_credential_value('aws_session_token')

hdr = {"Accept":"application/vnd.github+json","Authorization":f"Bearer {TOKEN}"}
r_key = requests.get(f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/public-key", headers=hdr)
r_key.raise_for_status()

j = r_key.json()
pk, kid = j['key'], j["key_id"]
pubkey = public.PublicKey(pk.encode(), encoding.Base64Encoder())

enc = public.SealedBox(pubkey).encrypt(SECRET_AWS_ACCESS_KEY_ID.encode())
enc = b64encode(enc).decode()
r_put = requests.put(f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/{AWS_ACCESS_KEY_ID}",
                     headers=hdr, json={"encrypted_value": enc, "key_id": kid})
r_put.raise_for_status()

enc = public.SealedBox(pubkey).encrypt(SECRET_AWS_SECRET_ACCESS_KEY.encode())
enc = b64encode(enc).decode()
r_put = requests.put(f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/{AWS_SECRET_ACCESS_KEY}",
                     headers=hdr, json={"encrypted_value": enc, "key_id": kid})
r_put.raise_for_status()

enc = public.SealedBox(pubkey).encrypt(SECRET_AWS_SESSION_TOKEN.encode())
enc = b64encode(enc).decode()
r_put = requests.put(f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/{AWS_SESSION_TOKEN}",
                     headers=hdr, json={"encrypted_value": enc, "key_id": kid})
r_put.raise_for_status()

print("[GitHub] Secrets aggiornati!")
