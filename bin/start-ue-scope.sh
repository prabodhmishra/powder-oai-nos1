#!/bin/bash

set -eux
cd /local/openairinterface5g/cmake_targets/lte_build_oai/build || exit
sudo ./lte-uesoftmodem -C 2685000000 -r 25 --ue-rxgain 120 --ue-txgain 20 --ue-max-power 0 --ue-scan-carrier -d --nokrnmod 1 --noS1 2>&1 | tee /tmp/ue.log
