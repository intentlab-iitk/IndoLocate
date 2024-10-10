#!/bin/sh

FNAME=$1
if [ "$FNAME" = "" ]; then
  echo "Missing filename"
  exit 1
fi

IFACE=$2
if [ "$IFACE" = "" ]; then
  echo "Missing interface"
  exit 1
fi

./tcpdump -i $IFACE -w /tmp/${FNAME} port 5500 
