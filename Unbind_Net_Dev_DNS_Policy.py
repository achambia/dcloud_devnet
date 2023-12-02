import requests
from requests.auth import HTTPBasicAuth

token = requests.post("https://api.umbrella.com/auth/v2/token", auth=HTTPBasicAuth('94cc871039a9427ca542fb38d312ca9d','afef2da4115e4299a2b87432ed8ab7ae'))
def bind_to_umb_policy(policy_name,policy_device):
    headers = {"Accept": "application/json",
               "Authorization": "Bearer " + f"{token.json()['access_token']}"}
    net_dev = requests.get("https://api.umbrella.com/deployments/v2/networkdevices", headers=headers)
    policy_id = requests.get("https://api.umbrella.com/deployments/v2/policies", headers=headers)
    for dev in policy_device:
        for x in net_dev.json():
            if dev in x['name']:
                for y in policy_id.json():
                    if policy_name == y['name']:
                        net_dev_bind = requests.delete(
                            f"https://api.umbrella.com/deployments/v2/policies/{y['policyId']}/identities/{x['originId']}",
                            headers=headers)
                        print(f"!! UNBINDING THE NETWORK DEVICE {x['name']} FROM THE DNS SECURITY POLICY {y['name']} !! \n")
                        if net_dev_bind.status_code == 200:
                            print("!! SUCCESS !! \n ")
                            print(f"!! DELETING THE NETWORK DEVICE {x['originId']} !! \n")
                            net_dev_del = requests.delete(f"https://api.umbrella.com/deployments/v2/networkdevices/{x['originId']}",
                                                   headers=headers)
                        else:
                            print("!! FAILURE IN BINDING NETWORK DEVICE TO DNS POLICY !!")
                    else:
                        continue
            else:
                continue


