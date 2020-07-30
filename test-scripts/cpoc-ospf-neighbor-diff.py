from genie.conf.base import Device
import json
import fnmatch


dev = Device(name='aName', os='ios')
dev.custom.abstraction = {'order':['os']}# Connect to device

import os
directory = './verifications/pre_upgrade/'
post_directory = './verifications/post_upgrade/'

def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True
print("Starting checks...")

for filename in os.listdir(directory):
    if fnmatch.fnmatch(filename, "*show_ip_ospf_neighbor_detail*_RAW.txt"):
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
        print(filename)
        command = command.replace("_"," ")

        print(pre_filename)
        print(post_filename)
        print(command)

        with open(pre_filename, newline='') as f:                        # Open show command list
            output = f.read()
            print(output)
            if  isBlank(output) == False:
                output = dev.parse(command, output=output)
                print(json.dumps(output))
            else:
                continue

        with open(post_filename, newline='') as f:
            output = f.read()
            print(output)

            if isBlank(output) == False:
                output = dev.parse(command, output=output)
                print(json.dumps(output))
            else:
                continue


        continue
    else:
        continue
