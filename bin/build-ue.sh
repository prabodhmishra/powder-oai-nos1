#!/bin/bash

cd /local/openairinterface5g/ || exit
git checkout v1.2.1
source oaienv
cd /local/openairinterface5g/cmake_targets || exit
./build_oai -I -w USRP --UE
