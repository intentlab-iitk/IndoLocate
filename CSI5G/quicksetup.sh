#!/bin/sh

echo "Configuring 5GHz band"
./config5GHZ.sh 157 80 1 1 1
echo "Adding filter for capturing CSI"
./setsourceinfo.sh eth7
