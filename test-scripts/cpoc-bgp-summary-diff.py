from genie.conf.base import Device
import json
import fnmatch


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
print("Starting checks...")

for filename in os.listdir(directory):
    if fnmatch.fnmatch(filename, "*show_bgp_all_summary*_RAW.txt"):
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
                pre = len(output["vrf"]["default"]["neighbor"])
                print(json.dumps(output))

                count = count + 1

            else:
                continue

        with open(post_filename, newline='') as f:
            output = f.read()
            if isBlank(output) == False:
                output = dev.parse(command, output=output)
                post = len(output["vrf"]["default"]["neighbor"])
            else:
                continue


            if pre == post:
                print("PASS: BGP neigbors check on device: " + device_name + " both versions have " + str(post) + " neighbors")
            elif pre < post:
                print("FAIL: BGP has gained a neighbor from upgrade on device: " + device_name)
            elif post < pre:
                print("FAIL: BGP has lost a neighbor from upgrade on device: " + device_name)



        continue
    else:
        continue

print(str(count) + " files processed")
