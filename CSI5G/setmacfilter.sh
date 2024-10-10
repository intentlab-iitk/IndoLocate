#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Usage: setmacfilter.sh interface frame_control mac_address"
  exit 1
fi

FCTL=$2
if [ "$FCTL" = "" ]; then
  echo "Missing frame control"
  exit 1
fi

MAC=$3
if [ "$MAC" = "" ]; then
  echo "Missing mac address"
  exit 1
fi

FCTL=$(echo $FCTL | sed -e "s/\:/\\\x/g")
MAC=$(echo $MAC | sed -e "s/\:/\\\x/g")
SEQUENCE="\x${FCTL}\x${MAC}"

./nexutil -I ${IFACE} -s 550 -b -l 8 -v `printf "${SEQUENCE}" | openssl enc -base64 | tr -d "\n"`
