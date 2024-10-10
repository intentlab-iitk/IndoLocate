#!/bin/sh

SLEEP="usleep 200000"
THISFOLDER="/jffs/CSI5G"

if [ ! -f "$THISFOLDER/rtecdc.bin" ]; then
  echo "Missing 5GHz firmware, terminating"
  exit 1
fi

echo "Removing 2.4GHz and 5GHz modules"
/sbin/rmmod wl
$SLEEP
/sbin/rmmod dhd
$SLEEP

echo "Reinserting 2.4GHz module"
/sbin/insmod wl.ko intf_name=eth6 instance_base=0
$SLEEP

echo "Reinserting 5GHz module"
/sbin/insmod /lib/modules/4.1.52/extra/dhd.ko firmware_path=${THISFOLDER}/rtecdc.bin instance_base=1

echo "Restaring and reconfiguring wireless"
/sbin/restart_wireless 2>/dev/null

echo "Removing interfaces from bridge"
/bin/brctl delif br0 eth6
/bin/brctl delif br0 eth7
