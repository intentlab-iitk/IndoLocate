#!/bin/sh

IFACE5GHZ="eth7"
WL="/usr/sbin/wl -i ${IFACE5GHZ}"

CHAN=$1
if [ "$CHAN" = "" ]; then
  echo "Run ./config5GHz channel bandwidth rxcore rxnss txcore"
  exit 1
fi

BW=$2
if [ "$BW" = "" ]; then
  echo "Missing bandwidth [20|40|80|160]"
  exit 1
fi

case "$BW" in
20)
  ;;
40)
  ;;
80)
  ;;
160)
  ;;
*)
  echo "Invalid bandwidth"
  exit 1
esac

RXCORE=$3
if [ "$RXCORE" = "" ]; then
  echo "Missing rxcore mask: set to combination (or) of values [1|2|4|8]"
  exit 1
fi
if [ "$RXCORE" -lt "1" -o "$RXCORE" -gt "15" ]; then
  echo "Invalid rxcore"
  exit 1
fi

RXNSS=$4
if [ "$RXNSS" = "" ]; then
  echo "Missing rxnss mask: set to combination (or) of values [1|2|4|8]"
  exit 1
fi
if [ "$RXNSS" -lt "1" -o "$RXNSS" -gt "15" ]; then
  echo "Invalid rxnss"
  exit 1
fi

TXCORE=$5
if [ "$TXCORE" = "" ]; then
  echo "Missing txcore: set to combination (or) of values [1|2|4|8]"
  exit 1
fi
if [ "$TXCORE" -lt "1" -o "$TXCORE" -gt "15" ]; then
  echo "Invalid txcore"
  exit 1
fi

SLEEP="usleep 100000"

# try running AP mode but check channel is configured correctly
while [ true ]; do
  # try changing channel just to learn channel code
  TARGETCHAN=$(wl -i $IFACE5GHZ chanspec "${CHAN}/${BW}" | awk -F"to " '{ print $2 }')
  ./runap.sh $IFACE5GHZ $CHAN $BW
  # CURCHAN=$($WL chanspec | awk '{ print $1 }')
  CURCHAN=$(wl -i $IFACE5GHZ chanspec | awk -F"(" '{ print $2}' | tr /\)/ /Z/)
  if [ "$CURCHAN" = "${TARGETCHAN}Z" ]; then
    break
  fi
  $SLEEP
  echo "Channel did not settle, reconfiguring..."
done

$SLEEP
./settxcore.sh $IFACE5GHZ $TXCORE
$SLEEP
./setcsicore.sh $IFACE5GHZ $RXCORE
$SLEEP
./setcsinss.sh $IFACE5GHZ $RXNSS
$SLEEP
$WL ap 0
$SLEEP
$WL monitor 1
$WL shmem 0x1650 1
