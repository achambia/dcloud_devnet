
import requests
from requests.auth import HTTPBasicAuth
import json
token = requests.post("https://api.umbrella.com/auth/v2/token", auth=HTTPBasicAuth('94cc871039a9427ca542fb38d312ca9d','afef2da4115e4299a2b87432ed8ab7ae'))
def bind_to_umb_policy(policy_name,policy_device):
    headers = {"Accept": "application/json",
               "Authorization": "Bearer " + f"{token.json()['access_token']}"}
    net_dev = requests.get("https://api.umbrella.com/deployments/v2/networkdevices", headers=headers)
    policy_id = requests.get("https://api.umbrella.com/deployments/v2/policies", headers=headers)
    print(net_dev.json())
    print(policy_id.json())
bind_to_umb_policy('Site400 DNS Policy',['Site400-cE1'])