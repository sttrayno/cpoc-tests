from genie.conf.base import Device
import json
import fnmatch
import os

# INITALISE COUNTERS

test1passcount = 0
test1failcount = 0

test2passcount = 0
test2failcount = 0

filecount = 0

# Connect to 'dummy' pyats device

dev = Device(name='aName', os='ios')
dev.custom.abstraction = {'order':['os']}# Connect to device


# SET DIRECTORIES, COULD BE TAKEN IN AS CMD ARG

directory = './verifications/pre_upgrade/'
post_directory = './verifications/post_upgrade/'

predirectory = os.listdir(directory)
postdirectory = os.listdir(post_directory)

# Check if file is blank before reading and processing

def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True
print("Starting checks...")

for filename in os.listdir(directory):
    if fnmatch.fnmatch(filename, "*show_bgp_all_RAW.txt"):
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
                print(output["vrf"])
            else:
                continue

        with open(post_filename, newline='') as f:
            output = f.read()
            if isBlank(output) == False:
                output = dev.parse(command, output=output)
                print(output["vrf"])
            else:
                continue


        continue
    else:
        continue
