#!/bin/sh

PCAP=$1
if [ "$PCAP" = "" ]; then
  echo "Missing pcap filename"
  exit 1
fi

OUTPUT=$2
if [ "$OUTPUT" = "" ]; then
  echo "Missing mat output filename"
  exit 1
fi

./csireader -f /tmp/${PCAP} -o /tmp/${OUTPUT} -a
