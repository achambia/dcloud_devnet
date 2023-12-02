from Vmanage_Auth import Authentication
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time

Auth = Authentication()
jsessionid = Auth.get_jsessionid('198.18.133.200', '8443', 'admin', 'C1sco12345')
token = Auth.get_token('198.18.133.200', '8443', jsessionid)
if token is not None:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid}

def policy_delete(policy_name,dns_policy):
    response_global = requests.get(f'https://198.18.133.200:8443/dataservice/template/policy/security/',
                                    headers=header, verify=False)
    resp_dns_sec = requests.get(f'https://198.18.133.200:8443/dataservice/template/policy/definition/dnssecurity',
                                    headers=header, verify=False)
    for x in response_global.json()['data']:
        if x['policyName'] == policy_name:
            if x['mastersAttached'] == 0:
                response_global_delete = requests.delete(
                    f'https://198.18.133.200:8443/dataservice/template/policy/security/{x["policyId"]}',
                    headers=header, verify=False)
                if response_global_delete.status_code == 200:
                    print("!! POLICY DELETED SUCCESSFULLY !!")
                else:
                    print("!! SOMETHING WENT WRONG !!")
            else:
                print("!! Other Templates attached to the Policy, therefore not deleting !!")
    for y in resp_dns_sec.json()['data']:
        if y['name'] == dns_policy:
            resp_dns = requests.delete(
                f'https://198.18.133.200:8443/dataservice/template/policy/definition/dnssecurity/{y["definitionId"]}',
                headers=header, verify=False)

            if resp_dns.status_code == 200:
                print("!! POLICY DELETED SUCCESSFULLY !!")
            else:
                print("!! SOMETHING WENT WRONG !!")

        else:
            print("!! Other Templates attached to the Policy, therefore not deleting !!")



