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

def getRoutes(bgpAll):
    bgpRoutes = {}
    for vrf in bgpAll['vrf']:
        vrfName = vrf
        for route in bgpAll['vrf'][vrf]['address_family']:
            for routeid in bgpAll['vrf'][vrf]['address_family'][route]['routes']:
                bgpRoutes[vrfName] = routeid
    return bgpRoutes

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
                pre_bgpAll = getRoutes(output)
            else:
                continue

        with open(post_filename, newline='') as f:
            output = f.read()
            if isBlank(output) == False:
                output = dev.parse(command, output=output)
                post_bgpAll = getRoutes(output)

            else:
                continue

        if pre_bgpAll == post_bgpAll:
            print("TEST - PASS: The port-channels configured and operational statuses are the same pre and post upgrade. No further action required.")
        elif pre_bgpAll != post_bgpAll:
            print("TEST - FAIL: There is some inconsistencies between pre/post state of the port channel config, see details of differences below.")

            for diff in list(dictdiffer.diff(pre_bgpAll, post_bgpAll)):
                print(diff)

    else:
        continue
