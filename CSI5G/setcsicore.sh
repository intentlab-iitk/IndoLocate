#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Missing interface"
  exit 1
fi

CORE=$2
if [ "$CORE" = "" ]; then
  echo "Missing core"
  exit 1
fi

./nexutil -I ${IFACE} -s 541 -l 4 -i -v $CORE
