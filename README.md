# Collection of CPOC pyATS tests

This repo contains a collection of pre/post validation checks for migrations build ontop of the pyATS framework. These tests can be used post change of a network to ensure aspects of the device control plane are unchanged following a test

Today the tests included are:

```
ARP table consistency
BGP neighbours consistency
BGP route validation
Etherchannel consistency
CDP neighbours table validation
```

### Pre-requsites

To run this script you will need your raw outputs from the devices in two directories `/pre_upgrade` and `post-upgrade`. Then ensure files within each directory adhere to the following format to ensure that our parsers sucessfully pick up your device outputs: ```<pre/post>_<device_name>_<command>_RAW.txt```

For example

```
/pre_upgrade
  pre_device-show_cdp_neighbors_detail_RAW.txt
/post_upgrade
  post_device-show_cdp_neighbors_detail_RAW.txt
```

These scripts have Python requirements that must be installed before the script will run. To this simply run the below command while in the same directory as our requirements.txt file.

```
pip install requirements.txt
```

### Tests

#### ARP Table checking

This script looks to read all ouputs from "show ip arp vrf" from the pre and post directories and runs two tests. The first which counts how many entries the ARP table has pre and post test and a second test which takes the IP to MAC mappings and stores them in a specific dictionary. This then does a comparison to check which elements are missing or have been changed. You might expect this to fail if hardware has been migrated,

#### BGP neighbours conistency

This script takes the raw output from a "show bgp summary" and runs two tests. The first which tests how many BGP neighbors a device has pre and post and makes a comparison and a second test which takes the actual neighbour ID's and does a comparison between pre and post check to see which elements have been added or are missing.

#### BGP route validation

This script takes the raw output from "show BGP all" and runs a single test. It checks which BGP routes have been discovered by the device on the device pre and post change versions across all VRF's. If there is any difference this will be outputed to the user.

#### Etherchannel consistency

This script takes the raw output from "show etherchannel summary" and runs two tests. The first which checks how many port groups are configured on the device pre and post change. Then a second then extracts the name of the port-channel and its current status "up/down" and does a comparison between the pre and post state to check if the state is any different post change. If there are any changes this is shown to the user.

#### CDP neigbours table validation

This script takes the raw output from "show cdp neighbors detail" and runs two tests. The first which checks how many CDP neighbours have been discovered by the device on the device pre and post change versions. Then a second then extracts the device_id and it's management IP and does a comparison between the pre and post state to check if the state is any different post change. If there are any changes this is shown to the user.

