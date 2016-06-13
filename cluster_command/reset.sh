#!/bin/bash
pkill -9 python
sleep 4
nohup python /home/ubuntu/remote-command-server.py &
