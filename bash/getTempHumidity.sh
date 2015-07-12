#!/bin/bash
if [ "$#" != 1 ]; then
  echo "Need to pass BLE Address $0 <BLE Address>"
else
  echo "Turning on Temperature and Humidity Sensor"
  gatttool -b $1 --char-write-req --handle=0x2C --value=01
  echo "Getting Temperature and Humidity"
  for i in `seq 1 10`;
  do
    sleep 1
    str=`gatttool -b $1 --char-read --handle=0x29`
    # Discard everything up to and including the ": " in the gatttool
    # response.  Put the four bytes returned into an array.  Then
    # swap the bytes and put the results in a variable.  Use bc to compute
    # the temp and humdity to allow for two decimal places.
    IFS=' ' read -a array <<< ${str#*: }
    temp="0x${array[1]}${array[0]}"
    temp=$((temp))
    humidity="0x${array[3]}${array[2]}"
    humidity=$((humidity))
    printf "temp: %s, humidity: %s\n" \
      `echo "scale=4; ($temp/65536*165-40)*1.8+32" | bc -l` \
      `echo "scale=4; ($humidity*1.0/65536.0)*100.0" | bc -l`
  done
  echo "Turning off Temperature and Humidity Sensor"
  gatttool -b $1 --char-write-req --handle=0x2C --value=00
fi
