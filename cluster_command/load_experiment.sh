#!/bin/bash
./remote-command.py "python /home/ubuntu/scootplayer/scootplayer.py -m http://192.168.1.235/dash/bunny360/bunny360.mpd --timeout 5" --360 &
./remote-command.py "python /home/ubuntu/scootplayer/scootplayer.py -m http://192.168.1.235/dash/bunny720/bunny720.mpd --timeout 5" --720 &
./remote-command.py "python /home/ubuntu/scootplayer/scootplayer.py -m http://192.168.1.235/dash/bunny1080/bunny1080.mpd --timeout 5" --1080 &
