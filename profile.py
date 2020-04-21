#!/usr/bin/env python

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN


tourDescription = """

This profile allocates hardware resources for deploying an OAI eNB and UE in
**noS1** mode (no core network) in a controlled RF environment on the POWDER
platform. The inlcuded scripts automate node setup, building the OAI binaries,
and starting the nework. The steps followed in these scripts are largely based
on
[this](https://gitlab.eurecom.fr/oai/openairinterface5g/wikis/HowToConnectOAIENBWithOAIUEWithoutS1Interface)
tutorial.

The following nodes will be deployed with the TX/RX and RX2 ports on the B210s
connected via an attenuator matrix:

* Intel NUC5300/B210 w/ OAI UE (`rue1`)
* Intel NUC5300/B210 w/ OAI eNB (`enb1`)

"""

tourInstructions = """

#### Preliminary setup after the experiment becomes ready

After the nodes boot for the first time, do the following on `rue1` and `enb`:

```
cd /local/repository
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
cd /local/repository
./start.sh
```

After both nodes start, the `enb1` will have a tunnel interface `oaitun_enb`
with IP address `10.0.1.1`, and `rue1` (if it has succussfully synchronized with
`enb1`) will have a tunnel interface `oaitun_ue1` with IP address `10.0.1.2`.
You can test the link using these IP addresses.

"""


class GLOBALS(object):
    UBUNTU_1804_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
    UBUNTU_1804_LOW_LATENCY_IMG = "urn:publicid:IDN+emulab.net+image+PowderProfiles:ubuntu1804lowlatency:1"
    NUC_HWTYPE = "nuc5300"


pc = portal.Context()
pc.bindParameters()
pc.verifyParameters()

request = pc.makeRequestRSpec()

# Add a NUC eNB node
enb1 = request.RawPC("enb1")
enb1.hardware_type = GLOBALS.NUC_HWTYPE
enb1.disk_image = GLOBALS.UBUNTU_1804_LOW_LATENCY_IMG
enb1.Desire("rf-controlled", 1)
enb1_rue1_rf = enb1.addInterface("rue1_rf")

# Add a NUC UE node
rue1 = request.RawPC("rue1")
rue1.hardware_type = GLOBALS.NUC_HWTYPE
rue1.disk_image = GLOBALS.UBUNTU_1804_LOW_LATENCY_IMG
rue1.Desire("rf-controlled", 1)
rue1_enb1_rf = rue1.addInterface("enb1_rf")

# Create the RF link between the UE and eNodeB
rflink = request.RFLink("rflink")
rflink.addInterface(enb1_rue1_rf)
rflink.addInterface(rue1_enb1_rf)

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
