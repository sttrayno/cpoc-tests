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

# Extract port-channel name and operational status from the dictionary and place into a new dictionary for further comparison

def returnPC(etherchannel_summary):
    pc_name = {}
    for key in etherchannel_summary['interfaces']:
        name = etherchannel_summary['interfaces'][key]['name']
        oper_status = etherchannel_summary['interfaces'][key]['oper_status']
        pc_name[name] = oper_status

    return pc_name

# Open each file in pre/post dictionary and select all show etherchannel summary raw outputs

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

        with open(pre_filename, newline='') as f:                        #
            output = f.read()
            if  isBlank(output) == False:
                output = dev.parse(command, output=output)
                pre = output["number_of_aggregators"]
                pre_pc_name = returnPC(output)
                filecount += 1
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
                print("TEST 1 - PASS: Port channel groups are the same: " + device_name + "      "  + str(pre) + "/" + str(post))
            elif pre < post:
                print("TEST 1 - FAIL: Port channel groups in pre-upgrade state " + str(pre) + " is less than the post-upgrade state " + str(post) + " device: " + device_name )
            elif post < pre:
                print("TEST 1 - FAIL: Port channel groups in post-upgrade state " + str(post) + " is less than the pre-upgrade state " + str(pre) + " on device: " + device_name )

            if pre_pc_name == post_pc_name:
                print("TEST 2 - PASS: The port-channels configured and operational statuses are the same pre and post upgrade. No further action required.")
            elif pre_pc_name != post_pc_name:
                print("TEST 2 - FAIL: There is some inconsistencies between pre/post state of the port channel config, see details of differences below.")
                for diff in list(dictdiffer.diff(pre_pc_name, post_pc_name)):
                    print(diff)

print(str(filecount) + " files processed")
