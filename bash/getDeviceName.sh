#!/bin/bash
if [ "$#" != 1 ]; then
  echo "Need to pass BLE Address $0 <BLE Address>"
else
  # Discard everything up to and including the ": " in the 
  # gatttool response.  Put the bytes returned into an array.  
  # Convert the bytes to ascii and print out.
  str=`gatttool -b $1 --char-read --handle=0x3`
  IFS=' ' read -a array <<< ${str#*: }
  for element in "${array[@]}"
  do 
    printf "\x$(printf "%x" "0x$element")"
  done
  echo
fi