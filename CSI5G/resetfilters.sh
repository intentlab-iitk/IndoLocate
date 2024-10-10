#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Missing interface"
  exit 1
fi

./nexutil -I $IFACE -s557 -l 4 -i -v0x0

