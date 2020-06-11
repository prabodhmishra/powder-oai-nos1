#!/usr/bin/env bash

# Run appropriate setup script with tracer

NODE_ID=$(geni-get client_id)

if [ $NODE_ID = "rue1" ]; then
    /local/repository/bin/start-ue-tracer.sh
elif [ $NODE_ID = "enb1" ]; then
    /local/repository/bin/start-enb-tracer.sh
else
    echo "no setup necessary"
fi
