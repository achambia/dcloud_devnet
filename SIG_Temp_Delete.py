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

def SIG_temp_delete(sig_tunnel_name,sig_cred_name):
    print('!! Verfying the SIG Templates are attached to other Device templates !! \n')
    response_global_all_feature_temp = requests.get(f'https://vManage_IP:vManage_Port/dataservice/template/feature?summary=true',
                                   headers=header, verify=False)
    for x in response_global_all_feature_temp.json()['data']:
        if x['templateName'] == sig_tunnel_name:
            response_global_sig_tunnel = requests.get(
                f'https://vManage_IP:vManage_Port/dataservice/template/feature/object/{x["templateId"]}',
                headers=header, verify=False)
            print("!! Deleting the SIG Tunnel Template as Template not attached to device !!\n")
            if response_global_sig_tunnel.json()['attachedMastersCount'] == 0:
                requests.delete(
                    f'https://vManage_IP:vManage_Port/dataservice/template/feature/{x["templateId"]}',
                    headers=header, verify=False)
        elif x['templateName'] ==sig_cred_name:
            response_global_sig_cred = requests.get(
                f'https://vManage_IP:vManage_Port/dataservice/template/feature/object/{x["templateId"]}',
                headers=header, verify=False)
            print("!! Deleting the SIG Credentials Template as Template not attached to device !!\n")
            if response_global_sig_cred.json()['attachedMastersCount'] == 0:
                requests.delete(
                    f'https://vManage_IP:vManage_Port/dataservice/template/feature/{x["templateId"]}',
                    headers=header, verify=False)

