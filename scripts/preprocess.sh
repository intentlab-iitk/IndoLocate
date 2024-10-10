#!/bin/bash

# Default arguments if none are provided
IP_ARG="trace.cap"
OUT_ARG="data.mat"

# Check if input argument is provided
if [ $# -ge 1 ]; then
    IP_ARG="$1"
fi

# Check if output argument is provided
if [ $# -ge 2 ]; then
    OUT_ARG="$2"
fi

# Run csireader with the provided or default arguments
./csireader -f "captureData/$IP_ARG" -o "matlabData/$OUT_ARG" -a
