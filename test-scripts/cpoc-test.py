from genie.testbed import load
import json
import csv

tb = load('./CPOCtestbed.yaml')                                                 # Load testbed file
dev = tb.devices['mkt-lnp6-csr1']                                               # Specify device from tb file
dev.connect()                                                                   # Connect to device

with open('verification commands.csv', newline='') as f:                        # Open show command list
    reader = csv.reader(f)
    data = list(reader)

for x in range(len(data)):
    cmd = str(data[x])
    cmd = cmd[2:-2]

    filename = cmd.replace(" ","")
    filenameraw = filename + "_RAW"
    filenameops = filename + "_OPS"

    rawoutput = dev.execute(cmd)
    devoutput = dev.parse(cmd)

    f1= open(filenameraw,"w+")
    f2= open(filenameops,"w+")

    f1.write(str(rawoutput))
    f2.write(str(devoutput))

    f1.close()
    f2.close()
