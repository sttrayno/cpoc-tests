from genie.conf.base import Device
import json
import fnmatch
import dictdiffer
import os

# INITALISE COUNTERS

test1passcount = 0
test1failcount = 0

test2passcount = 0
test2failcount = 0

filecount = 0

# Connect to 'dummy' pyats device

dev = Device(name='aName', os='ios')
dev.custom.abstraction = {'order':['os']}

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

# Extract neighbor information from the show CDP output and place device_id and management address into a dictionary for later comparison

def returnIP(CDPTable):
    iplist = {}
    for key in CDPTable['index']:
        hostname =  CDPTable['index'][key]['device_id']
        for ipkey in CDPTable['index'][key]['management_addresses']:
            iplist[hostname] = ipkey

    return iplist

# Open each file in pre/post dictionary and select all show cdp neighbors detail outputs

for filename in os.listdir(directory):
    if fnmatch.fnmatch(filename, "*show_cdp_neighbors_detail*_RAW.txt"):
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

        with open(pre_filename, newline='') as f:
            output = f.read()
            if  isBlank(output) == False:
                output = dev.parse(command, output=output)
                preIP = returnIP(output)
                pre = len(output["index"])
                filecount += 1
            else:
                continue

        with open(post_filename, newline='') as f:
            output = f.read()
            if isBlank(output) == False:
                output = dev.parse(command, output=output)
                postIP = returnIP(output)
                post = len(output["index"])
            else:
                continue

# RUNNING TESTS AND OUTPUT TO USER

            print('=============================================================')
            print('===================== '+ device_name + ' tests ===============')


            if pre == post:
                print("TEST 1 - PASS: CDP neighbors count are the same on device: " + device_name + "   " + str(pre) +"/"+ str(post))
            elif pre < post:
                print("TEST 1 - FAIL: CDP neighbors count pre-upgrade: " + str(pre) + " is less than the post-upgrade state: " + str(post) + " on device: " + device_name)
            elif post < pre:
                print("TEST 1 - FAIL: CDP neighbors count in post-upgrade: " + str(post) + " is less than the pre-upgrade state: " + str(pre) + " on device: " + device_name)

            if preIP == postIP:
                print("TEST 1 - PASS: CDP neighbors device_ID and IP information are the same on device post upgade")
            elif preIP != postIP:
                print("TEST 1 - FAIL: CDP neighbors on device are different post upgrade, this may be expected if you've had a hardware change, see differences below: ")
                for diff in list(dictdiffer.diff(preIP, postIP)):
                    print(diff)

        continue
    else:
        continue

# CONFIRMATION OF FILES PROCESSED
x=0
while x < 5:
    print("==================================")
    x = x +1

print(str(filecount) + " files processed")
