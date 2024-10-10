#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Missing interface"
  exit 1
fi

./nexutil -I $IFACE -s558 -l4 -i -v0x1
