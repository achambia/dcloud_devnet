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


def bind_sig_to_device_temp(temp_name,sig_tunnel_name,sig_tunnel_des,ipsec_tunnel_primary_num,ipsec_tunnel_secondary_num,pri_source_int,sec_source_int,tracker_ip,umb_key,umb_secret,org,sig_cred_name,sig_cred_des):
    attached_devices = []
    attached_devices_name = []
    push_verification = ''
    #Creating SIG Tunnel Feature Template
    print("!! Creating SIG TUNNEL FEATURE TEMPLATE !! \n")
    payload = {"templateName":f"{sig_tunnel_name}","templateDescription":f"{sig_tunnel_des}","templateType":"cisco_secure_internet_gateway","deviceType":["vedge-CSR-1000v"],"templateMinVersion":"15.0.0","templateDefinition":{"vpn-id":{"vipObjectType":"object","vipType":"constant","vipValue":0},"interface":{"vipType":"constant","vipValue":[{"if-name":{"vipObjectType":"object","vipType":"constant","vipValue":f"ipsec{ipsec_tunnel_primary_num}","vipVariableName":"tunnel_if_name"},"auto":{"vipObjectType":"object","vipType":"constant","vipValue":"true"},"shutdown":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"false","vipVariableName":"tunnel_shutdown"},"description":{"vipObjectType":"object","vipType":"ignore","vipVariableName":"tunnel_description"},"ip":{"unnumbered":{"vipObjectType":"node-only","vipType":"constant","vipValue":"true"}},"tunnel-source-interface":{"vipObjectType":"object","vipType":"constant","vipValue":f"{pri_source_int}","vipVariableName":"tunnel_tunnel_source_interface"},"tunnel-destination":{"vipObjectType":"object","vipType":"constant","vipValue":"dynamic"},"application":{"vipObjectType":"object","vipType":"constant","vipValue":"sig"},"tunnel-set":{"vipObjectType":"object","vipType":"constant","vipValue":"secure-internet-gateway-umbrella"},"tunnel-dc-preference":{"vipObjectType":"object","vipType":"constant","vipValue":"primary-dc"},"tcp-mss-adjust":{"vipObjectType":"object","vipType":"constant","vipValue":1300,"vipVariableName":"tunnel_tcp_mss_adjust_"},"mtu":{"vipObjectType":"object","vipType":"notIgnore","vipValue":1400,"vipVariableName":"tunnel_mtu_"},"dead-peer-detection":{"dpd-interval":{"vipObjectType":"object","vipType":"constant","vipValue":10,"vipVariableName":"tunnel_dpd_interval"},"dpd-retries":{"vipObjectType":"object","vipType":"constant","vipValue":3,"vipVariableName":"tunnel_dpd_retries"}},"ike":{"ike-version":{"vipObjectType":"object","vipType":"constant","vipValue":2},"authentication-type":{"pre-shared-key-dynamic":{"vipObjectType":"node-only","vipType":"constant","vipValue":"true"}},"ike-rekey-interval":{"vipObjectType":"object","vipType":"ignore","vipValue":14400,"vipVariableName":"tunnel_ike_rekey_interval_"},"ike-ciphersuite":{"vipObjectType":"object","vipType":"ignore","vipValue":"aes256-cbc-sha1","vipVariableName":"tunnel_ike_ciphersuite"},"ike-group":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"14","vipVariableName":"tunnel_ike_group"}},"ipsec":{"ipsec-rekey-interval":{"vipObjectType":"object","vipType":"ignore","vipValue":3600,"vipVariableName":"tunnel_ipsec_rekey_interval"},"ipsec-replay-window":{"vipObjectType":"object","vipType":"ignore","vipValue":512,"vipVariableName":"tunnel_ipsec_replay_window"},"ipsec-ciphersuite":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"aes256-gcm","vipVariableName":"tunnel_ipsec_ciphersuite"},"perfect-forward-secrecy":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"none","vipVariableName":"tunnel_perfect_forward_secrecy"}},"tracker":{"vipObjectType":"object","vipType":"ignore","vipValue":"_empty"},"track-enable":{"vipObjectType":"object","vipType":"ignore","vipValue":"true"}},{"if-name":{"vipObjectType":"object","vipType":"constant","vipValue":f"ipsec{ipsec_tunnel_secondary_num}","vipVariableName":"tunnel_if_name"},"auto":{"vipObjectType":"object","vipType":"constant","vipValue":"true"},"shutdown":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"false","vipVariableName":"tunnel_shutdown"},"description":{"vipObjectType":"object","vipType":"ignore","vipVariableName":"tunnel_description"},"ip":{"unnumbered":{"vipObjectType":"node-only","vipType":"constant","vipValue":"true"}},"tunnel-source-interface":{"vipObjectType":"object","vipType":"constant","vipValue":f"{sec_source_int}","vipVariableName":"tunnel_tunnel_source_interface"},"tunnel-destination":{"vipObjectType":"object","vipType":"constant","vipValue":"dynamic"},"application":{"vipObjectType":"object","vipType":"constant","vipValue":"sig"},"tunnel-set":{"vipObjectType":"object","vipType":"constant","vipValue":"secure-internet-gateway-umbrella"},"tunnel-dc-preference":{"vipObjectType":"object","vipType":"constant","vipValue":"secondary-dc"},"tcp-mss-adjust":{"vipObjectType":"object","vipType":"constant","vipValue":1300,"vipVariableName":"tunnel_tcp_mss_adjust_"},"mtu":{"vipObjectType":"object","vipType":"notIgnore","vipValue":1400,"vipVariableName":"tunnel_mtu_"},"dead-peer-detection":{"dpd-interval":{"vipObjectType":"object","vipType":"constant","vipValue":10,"vipVariableName":"tunnel_dpd_interval"},"dpd-retries":{"vipObjectType":"object","vipType":"constant","vipValue":3,"vipVariableName":"tunnel_dpd_retries"}},"ike":{"ike-version":{"vipObjectType":"object","vipType":"constant","vipValue":2},"authentication-type":{"pre-shared-key-dynamic":{"vipObjectType":"node-only","vipType":"constant","vipValue":"true"}},"ike-rekey-interval":{"vipObjectType":"object","vipType":"ignore","vipValue":14400,"vipVariableName":"tunnel_ike_rekey_interval_"},"ike-ciphersuite":{"vipObjectType":"object","vipType":"ignore","vipValue":"aes256-cbc-sha1","vipVariableName":"tunnel_ike_ciphersuite"},"ike-group":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"14","vipVariableName":"tunnel_ike_group"}},"ipsec":{"ipsec-rekey-interval":{"vipObjectType":"object","vipType":"ignore","vipValue":3600,"vipVariableName":"tunnel_ipsec_rekey_interval"},"ipsec-replay-window":{"vipObjectType":"object","vipType":"ignore","vipValue":512,"vipVariableName":"tunnel_ipsec_replay_window"},"ipsec-ciphersuite":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"aes256-gcm","vipVariableName":"tunnel_ipsec_ciphersuite"},"perfect-forward-secrecy":{"vipObjectType":"object","vipType":"notIgnore","vipValue":"none","vipVariableName":"tunnel_perfect_forward_secrecy"}},"tracker":{"vipObjectType":"object","vipType":"ignore","vipValue":"_empty"},"track-enable":{"vipObjectType":"object","vipType":"ignore","vipValue":"true"}}],"vipObjectType":"tree","vipPrimaryKey":["if-name"]},"service":{"vipType":"constant","vipValue":[{"svc-type":{"vipObjectType":"object","vipType":"constant","vipValue":"sig"},"ha-pairs":{"interface-pair":{"vipType":"constant","vipObjectType":"tree","vipPrimaryKey":["active-interface","backup-interface"],"vipValue":[{"active-interface":{"vipObjectType":"object","vipType":"constant","vipValue":f"ipsec{ipsec_tunnel_primary_num}"},"backup-interface":{"vipObjectType":"object","vipType":"constant","vipValue":f"ipsec{ipsec_tunnel_secondary_num}"},"active-interface-weight":{"vipObjectType":"object","vipType":"constant","vipValue":1},"backup-interface-weight":{"vipObjectType":"object","vipType":"constant","vipValue":1},"priority-order":["active-interface","backup-interface","active-interface-weight","backup-interface-weight"]}]}},"umbrella-data-center":{"data-center-primary":{"vipObjectType":"object","vipType":"ignore","vipValue":"","vipVariableName":"vpn_umbprimarydc"},"data-center-secondary":{"vipObjectType":"object","vipType":"ignore","vipValue":"","vipVariableName":"vpn_umbsecondarydc"}}}],"vipObjectType":"tree","vipPrimaryKey":["svc-type"]},"tracker-src-ip":{"vipObjectType":"object","vipType":"constant","vipValue":f"{tracker_ip}","vipVariableName":"vpn_trackersrcip"}},"factoryDefault":False}
    response_global_sig_tunnel = requests.post(f'https://198.18.133.200:8443/dataservice/template/feature/',
                                   headers=header, verify=False,json=payload)
    #Creating SIG Credentials Feature Template
    print("!! Creating SIG CREDENTIALS FEATURE TEMPLATE !! \n")
    payload_sig = {"templateName":f"{sig_cred_name}","templateDescription":f"{sig_cred_des}","templateType":"cisco_sig_credentials","deviceType":["vedge-CSR-1000v"],"templateMinVersion":"15.0.0","templateDefinition":{"umbrella":{"api-key":{"vipObjectType":"object","vipType":"constant","vipValue":f"{umb_key}","vipVariableName":"system_api_key"},"api-secret":{"vipObjectType":"object","vipType":"constant","vipValue":f"{umb_secret}","vipVariableName":"system_api_secret","vipNeedsEncryption":True},"org-id":{"vipObjectType":"object","vipType":"constant","vipValue":f"{org}","vipVariableName":"system_org_id"}}},"factoryDefault":False}
    response_global_sig_creds = requests.post(f'https://198.18.133.200:8443/dataservice/template/feature/',
                                   headers=header, verify=False,json=payload_sig)

    devic_id=[]
    #Getting device Template information
    response_global = requests.get(f'https://198.18.133.200:8443/dataservice/template/device',
                                    headers=header, verify=False)
    for x in  (response_global.json()['data']):
        if x['templateName'] in temp_name:
            devic_id.append((x['templateId']))
    for y in devic_id:
        # Running Get to find all feature templates assigned to the Device Template
        print("!! RETREIVING THE FEATURE TEMPLATES FROM THE DEVICE TEMPLATE !! \n")
        response_global_device = requests.get(f'https://198.18.133.200:8443/dataservice/template/device/object/{y}',
                                              headers=header,
                                              verify=False,)
        device_temp = response_global_device.json()
        #Updating the Feature Templates to Device Template Values
        print("!! Updating the Feature Templates to Device Templates !! \n")
        for z in device_temp['generalTemplates']:
            if z['templateType'] == "cisco_vpn":
                response_local = requests.get(f'https://198.18.133.200:8443/dataservice/template/feature/object/{z["templateId"]}',
                                              headers=header,
                                              verify=False,)
                if response_local.json()['editedTemplateDefinition']['vpn-id']['vipValue'] == 0:
                    z['subTemplates'].append({"templateId": f"{response_global_sig_tunnel.json()['templateId']}",
                                                 "templateType": "cisco_secure_internet_gateway"})
        sig_creds = {"templateId": f"{response_global_sig_creds.json()['templateId']}", "templateType" : "cisco_sig_credentials" }
        device_temp['generalTemplates'].append(sig_creds)
        response_global_update = requests.put(f'https://198.18.133.200:8443/dataservice/template/device/{y}', headers=header,
                                       verify=False, json=device_temp)
        # Finding the devices attached to the device template
        for w in response_global_update.json()['data']['attachedDevices']:
            attached_devices.append(w['uuid'])
            attached_devices_name.append(w['host-name'])
        input_payload = {"templateId": y, "deviceIds": attached_devices, "isEdited": True, "isMasterEdited": True}
        # Updating Variables and retreiving the payload
        print("!! UPDATING PAYLOAD !! \n")
        response_global_input = requests.post(f'https://198.18.133.200:8443/dataservice/template/device/config/input/',
                                              headers=header, verify=False, json=input_payload)
        attach_pay = response_global_input.json()['data']
        for m in attach_pay:
            m.update({"csv-templateId": y})
        global_attach_payload = {"deviceTemplateList":[{"templateId":y,"device":attach_pay,"isEdited":True,"isMasterEdited":True}]}
        #Asking Vmanage to Push the Config

        response_global_attach = requests.post(f'https://198.18.133.200:8443/dataservice/template/device/config/attachfeature',
                                              headers=header, verify=False, json=global_attach_payload)
        while push_verification != 'done':
            # Verifying the Status of the task
            done_verification = requests.get(
                f'https://198.18.133.200:8443/dataservice/device/action/status/{response_global_attach.json()["id"]}',
                headers=header, verify=False, json=response_global_input.json())
            push_verification = done_verification.json()['summary']['status']
            print("!! VMANAGE PUSHING THE CONFIG !!! SLEEPING FOR 5 SECS\n")
            time.sleep(5)

        if "Failure" in done_verification.json()['summary']['count']:
            print(f"!!! {done_verification.json()['summary']['count']['Failure']} devices Failed  to update!!!")
        else:
            print("!! SUCCESS !!! \n")
    return attached_devices











#print(Create_SIG_Creds('0fd7efcbf63542f0a02810a9e34b5184','98fcd86ee3a24c9292dc877465dbf01d','3547960',"abhi","abhi"))
#print(Create_SIG_Tunnels('SIG',"SIG",'2','3','GigabitEthernet1','GigabitEthernet1','10.2.7.2/32'))

#print(bind_sig_to_device_temp('Branch_Dev_Temp_Site_400','SIG',"SIG",'2','3','GigabitEthernet1','GigabitEthernet1','10.2.7.2/32','0fd7efcbf63542f0a02810a9e34b5184','98fcd86ee3a24c9292dc877465dbf01d','3547960',"abhi","abhi"))