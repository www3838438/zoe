#!/bin/bash

if [ ! `which tmux` ]; then
	echo "This script uses the tmux terminal multiplexer, but it is not available in PATH"
	exit 1
fi

# Address for the Swarm API endpoint
SWARM_ADDRESS="swarm:2380"


sudo docker -H ${SWARM_ADDRESS} run -i -t --rm=true -e ZOE_SCHEDULER_SWARM=${SWARM_ADDRESS} zoerepo/zoe-scheduler
sudo docker -H ${SWARM_ADDRESS} run -i -t --rm=true zoerepo/zoe-client ./zoe-web.py