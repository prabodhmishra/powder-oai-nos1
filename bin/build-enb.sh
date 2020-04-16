#!/bin/bash

cd /local/openairinterface5g/ || exit

# copy and update config non-existent
if [ ! -f ~/enb.conf ]; then
    VLANIF=$(ifconfig | grep vlan | cut -d ":" -f1)
    VLANIP=$(ip addr list "$VLANIF" | grep "inet " | cut -d' ' -f6|cut -d/ -f1)
    EPCIP=$VLANIP

    cp /local/repository/etc/enb.conf /local/enb.conf
    sed -i -e "s/CI_MME_IP_ADDR/$EPCIP/" /local/enb.conf
    sed -i -e "s/CI_ENB_IP_ADDR/$VLANIP/" /local/enb.conf
    sed -i -e "s/eth0/$VLANIF/" /local/enb.conf
fi

git checkout v1.2.1
source oaienv
cd /local/openairinterface5g/cmake_targets || exit
./build_oai -I -w USRP --eNB
