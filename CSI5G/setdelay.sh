#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Usage: setmacfilter.sh interface frame_control mac_address"
  exit 1
fi

DELAY=$2
if [ "$DELAY" = "" ]; then
  echo "Missing delay"
  exit 1
fi

DELAYHI=$((DELAY/65536))
DELAYTMP=$((DELAYHI*65536))
DELAYLOW=$((DELAY-DELAYTMP))

/usr/sbin/wl -i $IFACE shmem 0x1620 $DELAYLOW
/usr/sbin/wl -i $IFACE shmem 0x1622 $DELAYHI
