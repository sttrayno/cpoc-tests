from genie.conf.base import Device
import json
import fnmatch
import dictdiffer


test1passcount = 0
test1failcount = 0

test2passcount = 0
test2failcount = 0

test3passcount = 0
test3failcount = 0


dev = Device(name='aName', os='ios')
dev.custom.abstraction = {'order':['os']}# Connect to device
count = 0
import os
directory = './verifications/pre_upgrade/'
post_directory = './verifications/post_upgrade/'

def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def returnIP(arpTable):
    arp_table = {}
    for key in arpTable['interfaces']:
        for ipkey in arpTable['interfaces'][key]['ipv4']['neighbors']:
            ip = arpTable['interfaces'][key]['ipv4']['neighbors'][ipkey]['ip']
            ll = arpTable['interfaces'][key]['ipv4']['neighbors'][ipkey]['link_layer_address']
            arp_table[ip] = ll

    return arp_table

predirectory = os.listdir(directory)
postdirectory = os.listdir(post_directory)

def Diff(li1, li2):
    return (list(set(li1) - set(li2)))

print(Diff(postdirectory, postdirectory))

for filename in os.listdir(directory):
    if fnmatch.fnmatch(filename, "*show_ip_arp_vrf*_RAW.txt"):
        pre_filename = directory + filename
        post_filename = post_directory + filename
        post_filename = post_filename.replace("pre","post", 1)
        command = filename
        command = command[:-8]
        indx = command.find("show")#position of 'I'
        vrfindx = command.find("vrf")#position of 'I'
        vrf = command[vrfindx:]
        command = command[indx:]
        command = command.replace("_"," ")


        with open(pre_filename, newline='') as f:
            output = f.read()
            a = output.find("% VRF")
            device_name = filename[:indx]
            device_name = device_name.replace('pre','',1)

            if a == 0 or isBlank(output) == True:
                pre = 0
                preIP = 0

            else:
                output = dev.parse(command, output=output)
                pre = len(output["interfaces"])
                preIP = returnIP(output)


                count = count + 1

        with open(post_filename, newline='') as f:
            output = f.read()
            a = output.find("% VRF")

            if a == 0 or isBlank(output) == True:
                post = 0
                postIP = 0
            else:
                output = dev.parse(command, output=output)
                post = len(output["interfaces"])
                postIP = returnIP(output)


            print('=============================================================')
            print('===================== '+ device_name + ' tests ===============')


            if pre == post:
                test1passcount = test1passcount + 1
                print("TEST 1 PASS: ARP table entrie count is the same on device: " + device_name + " for VRF: " + vrf + "     " +  str(pre) + " / " +  str(post))
            elif pre < post:
                test1failcount = test1failcount + 1
                print("TEST 1 FAIL: ARP table in pre-upgrade is less than the post-upgrade stateon device: " + device_name + " for VRF: " + vrf+ "     " + str(pre) + " / " + str(post))
            elif post < pre:
                print("TEST 1 FAIL: ARP table in post-upgrade is less than the pre-upgrade state on device: " + device_name +" for VRF: " + vrf+ "     " + str(pre) + " / " + str(pre))
                test1failcount = test1failcount + 1


            if preIP == postIP:
                test2passcount = test2passcount + 1
                print("TEST 2 PASS: ARP table entries for IP address are the same on device: " + device_name + " for VRF: " + vrf)
            elif preIP != postIP:
                print("TEST 2 FAIL: ARP table for the IP/MAC address mappings are different post upgrade on device: " + device_name + " for VRF: " + vrf + "See changed entries below: ")
                test2failcount = test2failcount + 1
                for diff in list(dictdiffer.diff(preIP, postIP)):
                    print(diff)


    else:
        continue

x=0
while x < 5:
    print("==================================")
    x = x +1

print("TEST 1 ARP table entry checking Pass count: " + str(test1passcount))
print("TEST 1 ARP table entry checking fail count: " + str(test1failcount))
print("TEST 2 IP consistency check Pass count: " + str(test2passcount))
print("TEST 2 IP consistency check fail count: " + str(test2failcount))
print("TEST 3 L2 consistency check Passcount: " + str(test3passcount))
print("TEST 3 L2 consistency check fail count: " + str(test3failcount))
