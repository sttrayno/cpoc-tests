from genie.conf.base import Device
import json
import fnmatch
import dictdiffer


dev = Device(name='aName', os='ios')
dev.custom.abstraction = {'order':['os']}# Connect to device

import os
directory = './verifications/pre_upgrade/'
post_directory = './verifications/post_upgrade/'
count = 0

def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True
print("Starting checks...")

def returnPC(etherchannel_summary):
    pc_name = {}
    for key in etherchannel_summary['interfaces']:
        name = etherchannel_summary['interfaces'][key]['name']
        oper_status = etherchannel_summary['interfaces'][key]['oper_status']
        pc_name[name] = oper_status

    return pc_name



for filename in os.listdir(directory):
    if fnmatch.fnmatch(filename, "*show_etherchannel_summary*_RAW.txt"):
        pre_filename = directory + filename
        post_filename = post_directory + filename
        post_filename = post_filename.replace("pre","post", 1)
        command = filename
        command = command[:-8]
        indx = command.find("show")#position of 'I'
        device_name = filename[:indx]
        command = command[indx:]
        device_name = device_name.replace("pre_","",1)
        device_name = device_name.replace("post_","",1)
        command = command.replace("_"," ")

        with open(pre_filename, newline='') as f:                        # Open show command list
            output = f.read()
            if  isBlank(output) == False:
                output = dev.parse(command, output=output)
                pre = output["number_of_aggregators"]
                pre_pc_name = returnPC(output)
                count = count + 1
            else:
                continue

        with open(post_filename, newline='') as f:
            output = f.read()
            if isBlank(output) == False:
                output = dev.parse(command, output=output)
                post = output["number_of_aggregators"]
                post_pc_name = returnPC(output)
            else:
                continue


            if pre == post:
                print("TEST 1 PASS: Port channel groups are the same: " + device_name + "      "  + str(pre) + "/" + str(post))
            elif pre < post:
                print("TEST 1FAIL: Port channel groups in pre-upgrade state " + str(pre) + " is less than the post-upgrade state " + str(post) + " device: " + device_name )
            elif post < pre:
                print("TEST 1 FAIL: Port channel groups in post-upgrade state " + str(post) + " is less than the pre-upgrade state " + str(pre) + " on device: " + device_name )

            if pre_pc_name == post_pc_name:
                print("TEST 2 PASS")
            elif pre_pc_name != post_pc_name:
                print("TEST 2 FAIL")
                for diff in list(dictdiffer.diff(pre_pc_name, post_pc_name)):
                    print(diff)

print(str(count) + " files processed")
