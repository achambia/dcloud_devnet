import csv
import time

import Add_SIG_Default_Route
import Bind_Net_Dev_DNS_Policy
import Policy_attachment_to_cedge
import Policy_deattachment_from_cedge
import Policy_deletion
import SIG_Creation
import SIG_Destroy
import SIG_Temp_Delete
import Umb_DNS_Only_Policy
import Umbrella_DNS_Credentials
import Unbind_Net_Dev_DNS_Policy
import delete_SIG_Default_Route

print("**********WELCOME TO SDWAN SECURITY POLICY AUTOMATION***********\n")
user_option = input("Please enter the path of your CSV File ::::::::: ")
with open(f"{user_option}") as file:
    heading = next(file)
    reader = csv.reader(file)
    for x in reader:
        if (len(x)) > 24:
            print("!! Invalid Input Colums ... Please check !!!")
        elif x[0] == 'add':
            if x[1] == 'DNS':
                print("!! Creating Umbrella Credentials \n")
                Umbrella_DNS_Credentials.dns_creds(x[2], x[3], x[4])
                print("!! Creating Security and DNS Policies !! \n")
                Umb_DNS_Only_Policy.dns_local_policy(x[5], x[6],Umb_DNS_Only_Policy.dns_policy(x[7], x[8],
                                                                                    x[9].split()))
                print("!! Attaching Policy to Device Template \n")
                devices = Policy_attachment_to_cedge.attach_policy_to_cedge(x[5],x[10].split())
                print("!! Attaching Network Device to DNS Policy in Umbrella !!")
                time.sleep(7)
                Bind_Net_Dev_DNS_Policy.bind_to_umb_policy(x[11],devices)
                print("!! WORKFLOW EXECUTED SUCCESSFULLY !!")
            elif x[1] =='SIG':
                print("!! CREATING SIG TUNNELS AND CREDENTIALS !!\n")
                attached_devices = SIG_Creation.bind_sig_to_device_temp(x[10].split(),x[13],x[14],x[15],x[16],x[17],x[18],x[19],x[20],x[21],x[4],x[22],x[23])
                print("!! ADDING SIG DEFAULT ROUTE TO ENTERED VPN'S !!\n")
                Add_SIG_Default_Route.default_route(x[10].split(),x[9].split(),attached_devices)
                print("!! WORKFLOW EXECUTED SUCCESSFULLY !!")



        elif x[0] == 'delete':
            if x[1] =="DNS":
                print("!! Deattaching the security policy from  the device template !!\n")
                devices_del=Policy_deattachment_from_cedge.deattach_policy_to_cedge(x[10].split())
                print("!! DELETING POLICY !! ")
                Policy_deletion.policy_delete(x[5],x[7])
                print("!! Unbinding the network Device Identity from the Policy !!")
                Unbind_Net_Dev_DNS_Policy.bind_to_umb_policy(x[11],devices_del)
                print("!! WORKFLOW EXECUTED SUCCESSFULLY !! ")
            elif x[1] =="SIG":
                print("!! Deattaching the SIG Templates from  the device template !!\n")
                attach_dev = SIG_Destroy.delete_sig(x[10].split(),x[13],x[22])
                delete_SIG_Default_Route.del_default_route(x[10].split(),x[9].split(),attach_dev)
                SIG_Temp_Delete.SIG_temp_delete(x[13],x[22])
                print("!! WORKFLOW EXECUTED SUCCESSFULLY !! ")







