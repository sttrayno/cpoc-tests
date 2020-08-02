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

directory = './verifications/pre_upgrade/'
post_directory = './verifications/post_upgrade/'

def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True
print("Starting checks...")


# Extract all BGP neigbors from the dictionary and sort into ordered list for later comparison

def getBGPneighbors(bgpSummary):
    neighbors = []
    for key in bgpSummary['vrf']['default']['neighbor']:
        neighbor = key
        neighbors.append(neighbor)
        neighbors.sort()
    return neighbors

# Open each file for show bgp all summary

for filename in os.listdir(directory):
    if fnmatch.fnmatch(filename, "*show_bgp_all_summary*_RAW.txt"):
        pre_filename = directory + filename
        post_filename = post_directory + filename

        post_filename = post_filename.replace("pre","post", 1)

        command = filename
        command = command[:-8]

        indx = command.find("show")

        device_name = filename[:indx]
        command = command[indx:]

        device_name = device_name.replace("pre_","",1)
        device_name = device_name.replace("post_","",1)

        command = command.replace("_"," ")

        with open(pre_filename, newline='') as f:                        # Open show command list
            output = f.read()
            if  isBlank(output) == False:
                output = dev.parse(command, output=output)
                pre = len(output["vrf"]["default"]["neighbor"])
                preNeighbors = getBGPneighbors(output)

                filecount += 1

            else:
                continue


        print('=============================================================')
        print('===================== '+ device_name + ' tests ===============')



        with open(post_filename, newline='') as f:
            output = f.read()
            if isBlank(output) == False:
                output = dev.parse(command, output=output)
                post = len(output["vrf"]["default"]["neighbor"])
                postNeighbors = getBGPneighbors(output)

            else:
                continue


            if pre == post:
                print("PASS: BGP neigbors check on device: " + device_name + " both versions have " + str(post) + " neighbors")
            elif pre < post:
                print("FAIL: BGP has gained neighbor(s) from upgrade on device: " + device_name)
            elif post < pre:
                print("FAIL: BGP has lost neighbor(s) from upgrade on device: " + device_name)


            if preNeighbors == postNeighbors:
                print("PASS: BGP neigbors check on device: " + device_name + " both have consistent neighbors list")
            elif preNeighbors != postNeighbors:
                print("FAIL: BGP has neighbors list is inconsistent on device: " + device_name)




        continue
    else:
        continue

print(str(count) + " files processed")
