#!/bin/bash

set -eux
echo "Starting host setup"
while ! wget -qO - http://repos.emulab.net/emulab.key | sudo apt-key add -
do
    echo Failed to get emulab key, retrying
done

while ! sudo add-apt-repository -y http://repos.emulab.net/powder-testing/ubuntu/
do
    echo Failed to get johnsond ppa, retrying
done

while ! sudo apt-get update
do
    echo Failed to update, retrying
done

while ! sudo DEBIAN_FRONTEND=noninteractive apt-get install -y libuhd-dev linux-tools-$(uname -r)
do
    echo Failed to get gnuradio, retrying
done

while ! sudo "/usr/lib/uhd/utils/uhd_images_downloader.py"
do
    echo Failed to download uhd images, retrying
done

cd /local || exit
while ! git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git
do
    echo Failed to clone openairinterface5g, retrying
done

set -ux
./tune-cpu.sh

echo "Host setup complete!"
