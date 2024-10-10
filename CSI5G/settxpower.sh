#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Missing interface"
  exit 1
fi

POWER=$2
if [ "$POWER" = "" ]; then
  echo "Missing power"
  exit 1
fi

VAL=$(printf "%d" 0x${POWER}${POWER}${POWER}${POWER})
./nexutil -I $IFACE -s 549 -l 4 -i -v $VAL
