After installing pigpiod follow ~/pigpio/pigpio-master/util/readme.md to make it a service starting at boot

For the IR controller:
sudo cp ./startup_systemd/ir-controller.service  /lib/systemd/system/ir-controller.service
sudo systemctl daemon-reload
sudo systemctl enable ir-controller.service
