from Vmanage_Auth import Authentication
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import sys
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

Auth = Authentication()
jsessionid = Auth.get_jsessionid('198.18.133.200', '8443', 'admin', 'C1sco12345')
token = Auth.get_token('198.18.133.200', '8443', jsessionid)
if token is not None:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid}

def dns_policy(dns_policy_name,dns_policy_des,match_vpn):
    #Getting Umbrella Credentials from Vmanage
    response_umb_id = requests.get(f'https://198.18.133.200:8443/dataservice/template/policy/list/umbrelladata/',
                                   headers=header, verify=False)
    payload = dict({"name": f"{dns_policy_name}", "type": "DNSSecurity", "description": f"{dns_policy_des}","definition": {"localDomainBypassList": {}, "matchAllVpn": False,
                    "targetVpns": [{"vpns": match_vpn, "umbrellaDefault": True, "localDomainBypassEnabled": True}],
                    "dnsCrypt": False, "umbrellaData": {"ref": f"{response_umb_id.json()['data'][0]['listId']}"}}})
    #Creating DNS Security Policy
    response_global = requests.post(f'https://198.18.133.200:8443/dataservice/template/policy/definition/dnssecurity',
                                   headers=header, verify=False, json=(payload))
    if response_global.status_code != 200:
        if "Duplicate policy detected with name" in response_global.json()['error']['details']:
            print("!! WARNING .. DNS POLICY WITH THE SAME NAME EXISTS !! \n")
            sys.exit()
        else:
            print("!! WARNING ... SOMETHING WENT WRONG !!")

    elif response_global.status_code == 200:
        print("!!! DNS Policy Created !!! \n")
        return response_global.json()['definitionId']



def dns_local_policy(dns_policy_name,dns_policy_des,dns_policy):
    payload = {"policyDescription":f"{dns_policy_des}","policyType":"feature","policyName":f"{dns_policy_name}","policyUseCase":"custom","policyMode":"unified","policyDefinition":{"assembly":[{"definitionId":f"{dns_policy}","type":"DNSSecurity"}],"settings":{}},"isPolicyActivated":False}
    #Creating the Security Policy with DNS Profile Attached
    print()
    response_global = requests.post(f'https://198.18.133.200:8443/dataservice/template/policy/security/',
                                    headers=header, verify=False, json=(payload))
    if response_global.status_code !=200:
        if "Security policy with name" in response_global.json()['error']['details']:
            print("!! WARNING .. LOCALIZED POLICY WITH THE SAME NAME EXISTS !! \n")
            sys.exit()
        else:
            print(response_global.text)
            print("!! WARNING ... SOMETHING WENT WRONG !!")
    else:
        print(response_global.text)



#vpn =["10","30"]

#dns_local_policy('abhiu','abhi',dns_policy('abhi','abhi',vpn))