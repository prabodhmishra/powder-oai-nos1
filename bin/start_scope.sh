#!/usr/bin/env bash

# Run appropriate setup script to start with softscope

NODE_ID=$(geni-get client_id)

if [ $NODE_ID = "rue1" ]; then
    /local/repository/bin/start-ue-scope.sh
elif [ $NODE_ID = "enb1" ]; then
    /local/repository/bin/start-enb-scope.sh
else
    echo "no setup necessary"
fi
