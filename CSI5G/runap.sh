#!/bin/sh

IFACE=$1
if [ "$IFACE" = "" ]; then
  echo "Missing interface"
  exit 1
fi

CHAN=$2
if [ "$CHAN" = "" ]; then
  echo "Missing channel"
  exit 1
fi

BW=$3
if [ "$BW" = "" ]; then
  echo "Missing bandwidth"
  exit 1
fi

SSID="CSI${IFACE}"
ID=$(ip addr s dev br0 | grep inet | awk -F"." '{ print $4 }' | awk -F"/" '{ print $1}')
IP="172.16.16.${ID}"
NM="255.255.255.0"
WL="/usr/sbin/wl -i ${IFACE}"
IFCONFIG="/sbin/ifconfig ${IFACE}"

$WL down
if [ "$CHAN" == 14 ]; then
  $WL country JP
elif [ "$CHAN" -lt 36 ]; then
  $WL country IT
else
  $WL country US
fi

# check if monitor is on and disable it
MONITOR=$($WL monitor)
if [ "$MONITOR" = "1" ]; then
  $WL monitor 0
fi

$WL up
$WL radio on
# $WL interference 0
$WL infra 1
$WL ap 1
# $WL bssid B0:6E:BF:63:45:08
$WL ssid $SSID
$WL bss down
$WL bss up
$IFCONFIG $IP netmask $NM up

# setting chanspec in 2.4GHz band is tricky because there are many combinations for bonding
# try some that will work
if [ "$CHAN" -lt 36 -a "$BW" = "40" ]; then
  if [ "$CHAN" -lt 8 ]; then
    $WL chanspec 2g${CHAN}/${BW}l
  else
    $WL chanspec 2g${CHAN}/${BW}u
  fi
else
  $WL chanspec ${CHAN}/${BW}
fi

CHAN=$($WL chanspec)
echo "Interface ${IFACE} is ap with IP=${IP} on channel ${CHAN}"

