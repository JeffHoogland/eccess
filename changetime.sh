#!/bin/bash
#Usage: ./changetime.sh <hours> <minutes> <seconds>
echo "changetime.sh"
date +%T -s "${1}:${2}:${3}"
