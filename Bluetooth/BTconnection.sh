#! /bin/bash

# Connection with OnePlus Two
#sudo bluez-test-device remove 7C:01:91:50:38:A3
#sudo bluez-simple-agent hci0 C0:EE:FB:5A:8A:C3 
#sudo bluez-test-device trusted C0:EE:FB:5A:8A:C3 yes

# Connection with iPhone 5
sudo bluez-simple-agent hci0 4C:8D:79:82:1A:84
sudo bluez-test-device trusted 4C:8D:79:82:1A:84 yes

# Connection with iPhone 6S Plus
# sudo bluez-test-device remove C0:EE:FB:5A:8A:C3
# sudo bluez-simple-agent hci0 7C:01:91:50:38:A3
# sudo bluez-test-device trusted 7C:01:91:50:38:A3 yes
