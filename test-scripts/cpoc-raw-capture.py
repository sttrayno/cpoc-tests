from genie.testbed import load
import json
import csv

#Load testbed and connect to a device

tb = load('./CPOCtestbed.yaml')
dev = tb.devices['mkt-lnp6-csr1']
dev.connect()

#Load verification commands to run

with open('verification commands.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

#Loop through commands list and save to file

for x in range(len(data)):
    cmd = str(data[x])
    cmd = cmd[2:-2]

    filename = cmd.replace(" ","")
    filenameraw = filename + "_RAW"

    rawoutput = dev.execute(cmd)

    f1= open(filenameraw,"w+")

    f1.write(str(rawoutput))
    f2.write(str(devoutput))

    f1.close()
    f2.close()
