#!/bin/bash

# Start eNB with Tracer

set -eux
cd /local/openairinterface5g/ || exit
source oaienv
cd /local/openairinterface5g/cmake_targets || exit
sudo -E ./lte_build_oai/build/lte-softmodem -O /local/repository/etc/enb.conf --nokrnmod 1 --noS1 --T_stdout 0 --eNBs.[0].rrc_inactivity_threshold 0 2>&1 | tee /tmp/enb.log
