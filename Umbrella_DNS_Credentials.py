from Vmanage_Auth import Authentication
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def dns_creds(apikey,secret,org):
    Auth = Authentication()
    jsessionid = Auth.get_jsessionid('198.18.133.200', '8443', 'admin', 'C1sco12345')
    token = Auth.get_token('198.18.133.200', '8443', jsessionid)
    if token is not None:
        header = {'Content-Type': "application/json", 'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        header = {'Content-Type': "application/json", 'Cookie': jsessionid}
    payload = {"name":"umbrellaTokenList","description":"","type":"umbrellaData","entries":[{"apiKey":apikey,"secret":secret,"umbOrgId":org,"token":""}]}
    #Sending Query to update the Umbrella Keys
    response_global = requests.post(f'https://198.18.133.200:8443/dataservice/template/policy/list/umbrelladata/',
                                   headers=header, verify=False, data=json.dumps(payload))
    if (response_global.status_code) == 200:
        print("!! UMBRELLA DNS CREDENTIALS CREATED !!\n")
    elif(response_global.json()['error']['details'] == 'Umbrella data entry already exists'):
        response_umb_id = requests.get(f'https://198.18.133.200:8443/dataservice/template/policy/list/umbrelladata/',
                                        headers=header, verify=False)
        response_umb = requests.put(f'https://198.18.133.200:8443/dataservice/template/policy/list/umbrelladata/{response_umb_id.json()["data"][0]["listId"]}',
                                        headers=header, verify=False, data=json.dumps(payload))
        if response_umb.status_code == 200:
            print("!! UMBRELLA DNS CREDENTIALS UPDATED !! \n")
        else:
            print("!! SOMETHING WENT WRONG WHILE UPDATING CREDENTIALS !!")
    else:
        print(response_global.json()['error']['details'])
        print(" !!!!!! WARNING !!!!!  SOMETHING WENT WRONG WHILE ADDING UMBRELLA CREDENTIALS TO VMANAGE\n")

