import requests
from requests.auth import HTTPBasicAuth

token = requests.post("https://api.umbrella.com/auth/v2/token", auth=HTTPBasicAuth('022624db256545ccaa269b598aade3b6','fd39f9761a964d9abd85a567c539405a'))
def bind_to_umb_policy(policy_name,policy_device):
    dev_range = 0
    headers = {"Accept": "application/json",
               "Authorization": "Bearer " + f"{token.json()['access_token']}"}
    net_dev = requests.get("https://api.umbrella.com/deployments/v2/networkdevices", headers=headers)
    policy_id = requests.get("https://api.umbrella.com/deployments/v2/policies", headers=headers)
    for dev in policy_device:
        for x in net_dev.json():
            if dev in x['name']:
                for y in policy_id.json():
                    if policy_name == y['name']:
                        net_dev_bind = requests.put(
                            f"https://api.umbrella.com/deployments/v2/policies/{y['policyId']}/identities/{x['originId']}",
                            headers=headers)
                        print(f"!! Binding the Network Device {x['name']} to the DNS Security policy {y['name']} !! \n")
                        if net_dev_bind.status_code == 200:
                            print("!! SUCCESS !! \n ")
                        else:
                            print("!! FAILURE IN BINDING NETWORK DEVICE TO DNS POLICY !!")
                    else:
                        continue
            else:
                continue





