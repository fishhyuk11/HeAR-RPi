#!/bin/bash

# vim /etc/modprobe.d/alsa-base.conf
sudo /sbin/alsa force-reload
cat /proc/asound/cards
