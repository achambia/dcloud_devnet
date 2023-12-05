from Vmanage_Auth import Authentication
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time

Auth = Authentication()
jsessionid = Auth.get_jsessionid('vManage_IP', 'vManage_Port', 'vManage_User', 'vManage_Password')
token = Auth.get_token('vManage_IP', 'vManage_Port', jsessionid)
if token is not None:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid}

def get_device_templates(temp_name):
    # Function to get the ID for Templates and enter it to the list
    devic_id=[]
    response_global = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/device',
                                    headers=header, verify=False)
    for x in  (response_global.json()['data']):
        if x['templateName'] in temp_name:
            devic_id.append((x['templateId']))
    return devic_id

def attach_policy_to_cedge(policy_name,temp_name):
    # Function to attach Security policy to the Device
    attached_devices = []
    attached_devices_name = []
    push_verification = ''
    local_policy = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/policy/security/',headers=header,
                                              verify=False,)
    for x in local_policy.json()['data']:
        if x['policyName'] == policy_name:
            policyid = x['policyId']
    print("!! FINDING THE POLICY ID !!\n")
    devic_id=[]
    response_global = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/device',
                                    headers=header, verify=False)
    for t in (response_global.json()['data']):
        if t['templateName'] in temp_name:
            devic_id.append((t['templateId']))


    for x in devic_id:
        # Running Get to find all feature templates assigned to the Device Template
        print("!! RETREIVING THE FEATURE TEMPLATES FROM THE DEVICE TEMPLATE !! \n")
        response_global_device = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/device/object/{x}',
                                              headers=header,
                                              verify=False,)
        device_temp = response_global_device.json()
        # appending the policy ID to the payload
        device_temp.update({"securityPolicyId":policyid})
        # Updating the device template with the security policy
        print("!! UPDATING THE DEVICE TEMPLATE WITH SECURITY POLICY !! \n")
        response_global = requests.put(f'https://vManage_IP:vManage_Port/dataservice/template/device/{x}',headers=header, verify=False,json=device_temp)
        # Finding the devices attached to the device template
        for y in response_global.json()['data']['attachedDevices']:
            attached_devices.append(y['uuid'])
            attached_devices_name.append(y['host-name'])
        input_payload = { "templateId" : x,"deviceIds" : attached_devices,"isEdited":True,"isMasterEdited":True}
        #Updating Variables and retreiving the payload
        print("!! UPDATING PAYLOAD !! \n")
        response_global_input = requests.post(f'https://vManage_IP:vManage_Port/dataservice/template/device/config/input/',headers=header, verify=False,json=input_payload)
        attach_pay = response_global_input.json()['data']
        for z in attach_pay:
            z.update({"csv-templateId": x})
        global_attach_payload = {"deviceTemplateList":[{"templateId":x,"device":attach_pay,"isEdited":True,"isMasterEdited":True}]}
        #Asking Vmanage to Push the Config
        response_global_attach = requests.post(f'https://vManage_IP:vManage_Port/dataservice/template/device/config/attachfeature',
                                              headers=header, verify=False, json=global_attach_payload)

        while push_verification != 'done':
            #Verifying the Status of the task
            done_verification = requests.get(
                f'https://vManage_IP:vManage_Port/dataservice/device/action/status/{response_global_attach.json()["id"]}',
                headers=header, verify=False, json=response_global_input.json())
            push_verification = done_verification.json()['summary']['status']
            print("!! VMANAGE PUSHING THE CONFIG !!! SLEEPING FOR 5 SECS\n")
            time.sleep(5)

        if "Failure" in done_verification.json()['summary']['count']:
            print(f"!!! {done_verification.json()['summary']['count']['Failure'] } devices Failed  to update!!!")
        else:
            print("!! SUCCESS !!! \n")
    return attached_devices_name
