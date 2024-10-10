#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Missing interface"
  exit 1
fi

./nexutil -I ${IFACE} -s 550 -b -l 8 -v `printf "\
\x88\x00\x00\x12\x34\x56\x78\x9b\
" | openssl enc -base64 | tr -d "\n"`

