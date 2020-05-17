#!/usr/bin/env bash

# Run appropriate setup script

NODE_ID=$(geni-get client_id)
NODE_TYPE=${NODE_ID:0:3}

if [ $NODE_TYPE = "rue" ]; then
    /local/repository/bin/start-ue.sh
elif [ $NODE_TYPE = "enb" ]; then
    /local/repository/bin/start-enb.sh
else
    echo "no setup necessary"
fi
