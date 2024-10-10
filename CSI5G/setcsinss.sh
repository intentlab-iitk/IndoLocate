#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Missing interface"
  exit 1
fi

NSS=$2
if [ "$NSS" = "" ]; then
  echo "Missing nss"
  exit 1
fi

./nexutil -I ${IFACE} -s 542 -l 4 -i -v $NSS
