#! /bin/bash

sudo bluez-simple-agent hci0 7C:01:91:50:38:A3
sudo bluez-test-device trusted 7C:01:91:50:38:A3 yes
