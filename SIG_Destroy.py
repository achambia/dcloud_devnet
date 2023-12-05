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


def delete_sig(temp_name,sig_tunnel_name,sig_cred_name):
    attached_devices = []
    attached_devices_name = []
    push_verification = ''
    response_global_all_feature_temp = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/feature?summary=true',
                                   headers=header, verify=False)
    for x in response_global_all_feature_temp.json()['data']:
        if x['templateName'] == sig_tunnel_name:
            response_global_sig_tunnel = requests.get(
                f'https://vManage_IP:vManage_Port/dataservice/template/feature/object/{x["templateId"]}',
                headers=header, verify=False)
        elif x['templateName'] ==sig_cred_name:
            response_global_sig_cred = requests.get(
                f'https://vManage_IP:vManage_Port/dataservice/template/feature/object/{x["templateId"]}',
                headers=header, verify=False)



    devic_id = []
    # Getting device Template information
    response_global = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/device',
                                   headers=header, verify=False)
    for t in (response_global.json()['data']):
        if t['templateName'] in temp_name:
            devic_id.append((t['templateId']))
    for y in devic_id:
        # Running Get to find all feature templates assigned to the Device Template
        print("!! RETREIVING THE FEATURE TEMPLATES FROM THE DEVICE TEMPLATE !! \n")
        response_global_device = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/device/object/{y}',
                                              headers=header,
                                              verify=False, )
        device_temp = response_global_device.json()
        # Updating the Feature Templates to Device Template Values
        print("!! Updating the Feature Templates to Device Templates !! \n")
        for z in device_temp['generalTemplates']:
            if z['templateType'] == "cisco_vpn":
                response_local = requests.get(
                    f'https://vManage_IP:vManage_Port/dataservice/template/feature/object/{z["templateId"]}',
                    headers=header,
                    verify=False, )
                if response_local.json()['editedTemplateDefinition']['vpn-id']['vipValue'] == 0:
                    z['subTemplates'].remove({"templateId": f"{response_global_sig_tunnel.json()['templateId']}",
                                              "templateType": "cisco_secure_internet_gateway"})
        sig_creds = {"templateId": f"{response_global_sig_cred.json()['templateId']}",
                     "templateType": "cisco_sig_credentials"}
        device_temp['generalTemplates'].remove(sig_creds)

        response_global_update = requests.put(f'https://vManage_IP:vManage_Port/dataservice/template/device/{y}',
                                              headers=header,
                                              verify=False, json=device_temp)
        # Finding the devices attached to the device template
        for w in response_global_update.json()['data']['attachedDevices']:
            attached_devices.append(w['uuid'])
            attached_devices_name.append(w['host-name'])
        input_payload = {"templateId": y, "deviceIds": attached_devices, "isEdited": True, "isMasterEdited": True}
        # Updating Variables and retreiving the payload
        print("!! UPDATING PAYLOAD !! \n")
        response_global_input = requests.post(f'https://vManage_IP:vManage_Port/dataservice/template/device/config/input/',
                                              headers=header, verify=False, json=input_payload)
        attach_pay = response_global_input.json()['data']
        for m in attach_pay:
            m.update({"csv-templateId": y})
        global_attach_payload = {
            "deviceTemplateList": [{"templateId": y, "device": attach_pay, "isEdited": True, "isMasterEdited": True}]}
        # Asking Vmanage to Push the Config

        response_global_attach = requests.post(
            f'https://vManage_IP:vManage_Port/dataservice/template/device/config/attachfeature',
            headers=header, verify=False, json=global_attach_payload)
        while push_verification != 'done':
            # Verifying the Status of the task
            done_verification = requests.get(
                f'https://vManage_IP:vManage_Port/dataservice/device/action/status/{response_global_attach.json()["id"]}',
                headers=header, verify=False, json=response_global_input.json())
            push_verification = done_verification.json()['summary']['status']
            print("!! VMANAGE PUSHING THE CONFIG !!! SLEEPING FOR 5 SECS\n")
            time.sleep(5)

        if "Failure" in done_verification.json()['summary']['count']:
            print(f"!!! {done_verification.json()['summary']['count']['Failure']} devices Failed  to update!!!")
        else:
            print("!! SUCCESS !!! \n")
        response_global_sig_tunnel = requests.post(f'https://vManage_IP:vManage_Port/dataservice/template/feature/',
                                                   headers=header, verify=False,)
        sig_tunnel_check = requests.get(
            f'https://vManage_IP:vManage_Port/dataservice/template/feature/object/{x["templateId"]}',
            headers=header, verify=False)




    return attached_devices


