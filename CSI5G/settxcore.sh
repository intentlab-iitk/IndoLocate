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

WL="/usr/sbin/wl -i ${IFACE}"
$WL txcore -k $CORE -o $CORE -s 1 -c $CORE
