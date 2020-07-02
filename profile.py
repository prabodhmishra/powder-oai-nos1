#!/usr/bin/env python

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN
import geni.urn as URN


tourDescription = """

This profile allocates hardware resources for deploying an OAI eNB and UE in
**noS1** mode (no core network) in a controlled RF environment on the POWDER
platform. The included scripts automate node setup, building the OAI binaries,
and starting the nework. The steps followed in these scripts are largely based on
[this](https://gitlab.eurecom.fr/oai/openairinterface5g/wikis/HowToConnectOAIENBWithOAIUEWithoutS1Interface)
tutorial.

The following nodes will be deployed with the TX/RX and RX2 ports on the B210s
connected via an attenuator matrix:

* Intel NUC5300/B210 w/ OAI UE (`rue1`)
* Intel NUC5300/B210 w/ OAI eNB (`enb1`)

"""

tourInstructions = """
[Link](https://gitlab.eurecom.fr/oai/openairinterface5g/wikis/HowToConnectOAIENBWithOAIUEWithoutS1Interface) to the related tutorial page on OAI GitLab page. 

#### Preliminary setup after the experiment becomes ready

After the nodes boot for the first time, do the following on `rue1` and `enb`:

```
cd /local/repository/bin
./setup.sh
./build.sh
```

This will install the necessary software and configuration files on each node.
It may take several minutes. The script will exit on error; make sure it
completes on both nodes before moving on. These changes will persist after
reboot.

#### Starting the end-to-end network

After the preliminary setup has completed without error, do the following, first
on `enb1`, and after a few moments on `rue1` (the order is important here):

```
cd /local/repository/bin
./start.sh
```

After both nodes start, the `enb1` will have a tunnel interface `oaitun_enb1`
with IP address `10.0.1.1`, and `rue1` (if it has succussfully synchronized with
`enb1`) will have a tunnel interface `oaitun_ue1` with IP address `10.0.1.2`.
You can test the link using these IP addresses.

**_From eNB node_**
```
ping -I oaitun_enb1 10.0.1.2 
```
**_From UE node_**
```
ping -I oaitun_ue1 10.0.1.1 
```

#### Using softscope to view traffic

After the build is successfully done, you can go to the build directory and compile softscope to use on the eNB and the UE nodes:

**_From eNB node:_**
```
cd /local/openairinterface5g/cmake_targets/lte_build_oai/build/
make enbscope
```
**_From UE node:_**
```
cd /local/openairinterface5g/cmake_targets/lte_build_oai/build/
make uescope
```
On each node after the `make` process finishes:
```
cd /local/repository/bin
./start_scope.sh
```

#### Using Tracer for monitoring
[Link](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/T/basic) to the related page on Tracers in OAI GitLab.
After the build is successfully done, you can go to the Tracer directory and compile it to use on the eNB and the UE nodes:

**_From eNB node:_**
```
cd /local/openairinterface5g/common/utils/T/tracer
make
./enb -d ../T_messages.txt
```
**_From UE node:_**
```
cd /local/openairinterface5g/common/utils/T/tracer
make
./ue -d ../T_messages.txt
```
On each node after the `make` process finishes:
```
cd /local/repository/bin
./start_tracer.sh
```

"""


class GLOBALS(object):
    UBUNTU_1804_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
    UBUNTU_1804_LOW_LATENCY_IMG = "urn:publicid:IDN+emulab.net+image+PowderProfiles:ubuntu1804lowlatency:1"
    UE_IMG  = URN.Image(PN.PNDEFS.PNET_AM, "PhantomNet:ANDROID444-STD")
    ADB_IMG = URN.Image(PN.PNDEFS.PNET_AM, "PhantomNet:UBUNTU14-64-PNTOOLS")
    NUC_HWTYPE = "nuc5300"
    UE_HWTYPE = "nexus5"


pc = portal.Context()

pc.defineParameter("UE_TYPE", "Choose UE type",
                   portal.ParameterType.STRING, "NUC",[("COTS","OTS UE"),("NUC","USE NUC5300")],
                   longDescription="Input the tupe of UE to use.")

params = pc.bindParameters()
pc.verifyParameters()

request = pc.makeRequestRSpec()

# Add a NUC eNB node
enb1 = request.RawPC("enb1")
enb1.hardware_type = GLOBALS.NUC_HWTYPE
enb1.disk_image = GLOBALS.UBUNTU_1804_LOW_LATENCY_IMG
enb1.Desire("rf-controlled", 1)
enb1_rue1_rf = enb1.addInterface("rue1_rf")

if params.UE_TYPE == "NUC": 
# Add a NUC UE node
    rue1 = request.RawPC("rue1")
    rue1.hardware_type = GLOBALS.NUC_HWTYPE
    rue1.disk_image = GLOBALS.UBUNTU_1804_LOW_LATENCY_IMG
    rue1.Desire("rf-controlled", 1)
    rue1_enb1_rf = rue1.addInterface("enb1_rf")
else:
    # Add a node to act as the ADB target host
    adb_t = request.RawPC("adb-tgt")
    adb_t.disk_image = GLOBALS.ADB_IMG

    # Add an OTS (Nexus 5) UE       
    rue1 = request.RawPC("rue1")
    rue1.hardware_type = GLOBALS.UE_HWTYPE
    rue1.disk_image = GLOBALS.UE_IMG
    rue1.Desire("rf-controlled", 1)
    rue1.adb_target = "adb-tgt"
    rue1_enb1_rf = rue1.addInterface("enb1_rf")

# Create the RF link between the UE and eNodeB
rflink = request.RFLink("rflink")
rflink.addInterface(enb1_rue1_rf)
rflink.addInterface(rue1_enb1_rf)

if params.UE_TYPE == "NUC": 
    link = request.Link("lan")
    link.addNode(rue1)
    link.addNode(enb1)
    link.link_multiplexing = True
    link.vlan_tagging = True
    link.best_effort = True

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)

pc.printRequestRSpec(request)
