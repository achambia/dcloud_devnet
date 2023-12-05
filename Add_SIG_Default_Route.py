from Vmanage_Auth import Authentication
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time

Auth = Authentication()
jsessionid = Auth.get_jsessionid('vManage_IP', 'vManage_Port', 'vManage_user', 'vManage_Password')
token = Auth.get_token('vManage_IP', 'vManage_Port', jsessionid)
if token is not None:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid}

def default_route(temp_name,vpn,attached_devices):
    devic_id = []
    # Getting device Template information
    response_global = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/device',
                                   headers=header, verify=False)
    for x in (response_global.json()['data']):
        if x['templateName'] in temp_name:
            devic_id.append((x['templateId']))
    for y in devic_id:
        # Running Get to find all feature templates assigned to the Device Template
        print("!! RETREIVING THE FEATURE TEMPLATES FROM THE DEVICE TEMPLATE !! \n")
        response_global_device = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/device/object/{y}',
                                              headers=header,
                                              verify=False, )
        device_temp = response_global_device.json()
        # Updating the Feature Templates to Device Template Values
        print("!! Updating the Feature Templates to Device Templates !! \n")
        print("!! Updating SIG Service Route !!\n")
        for z in device_temp['generalTemplates']:
            if z['templateType'] == "cisco_vpn":
                response_local = requests.get(
                    f'https://vManage_IP:vManage_Port/dataservice/template/feature/object/{z["templateId"]}',
                    headers=header,
                    verify=False, )
                #Add service SIG Route to each VRF

                for vrf in vpn:
                    push_verification = ''
                    if response_local.json()['editedTemplateDefinition']['vpn-id']['vipValue'] == int(vrf):
                        print(f"!! Adding SIG Route to VPN {vrf}!!\n")
                        response_local_vpn = requests.get(
                            f'https://vManage_IP:vManage_Port/dataservice/template/feature/object/{z["templateId"]}',
                            headers=header,
                            verify=False, )
                        update_payload = (response_local_vpn.json())
                        update_payload['templateDefinition']['ip'].update({"service-route":{"vipType":"constant","vipValue":[{"prefix":{"vipObjectType":"object","vipType":"constant","vipValue":"0.0.0.0/0","vipVariableName":"vpn_serviceroute_prefix"},"vpn":{"vipObjectType":"object","vipType":"constant","vipValue":0},"service":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"sig"},"priority-order":["prefix","vpn","service"]}],"vipObjectType":"tree","vipPrimaryKey":["prefix"]}})
                        response_local_dr = requests.put(
                            f'https://vManage_IP:vManage_Port/dataservice/template/feature/{z["templateId"]}',
                            headers=header,
                            verify=False, json=update_payload)
                        input_payload = {"templateId": y, "deviceIds": attached_devices, "isEdited": True,
                                         "isMasterEdited": True}
                        # Updating Variables and retreiving the payload
                        print("!! UPDATING PAYLOAD !! \n")
                        response_global_input = requests.post(
                            f'https://vManage_IP:vManage_Port/dataservice/template/device/config/input/',
                            headers=header, verify=False, json=input_payload)
                        attach_pay = response_global_input.json()['data']
                        for m in attach_pay:
                            m.update({"csv-templateId": y})
                        global_attach_payload = {"deviceTemplateList": [
                            {"templateId": y, "device": attach_pay, "isEdited": True, "isMasterEdited": True}]}
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
                            print(
                                f"!!! {done_verification.json()['summary']['count']['Failure']} devices Failed  to update!!!")
                        else:
                            print("!! SUCCESS !!! \n")
