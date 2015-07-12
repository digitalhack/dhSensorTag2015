#
# TI SimpleLink SensorTag 2015
# Date: 2015 07 06
#
# Sensor: Buttons
# Values: Notify when pressed
#
import struct, sys, traceback, signal, os
from bluepy.btle import UUID, Peripheral, BTLEException, DefaultDelegate

class MyDelegate(DefaultDelegate):
  def __init__(self, params):
    DefaultDelegate.__init__(self)
    print "Info, DefaultDelegate set", params

  def handleNotification(self, cHandle, data):
    global keys
    # print "Info, in MyDelegate: handleNotification"
    
    # Set global variable to the value returned in the
    # notification
    if int(cHandle) == keyPressState:
      keys = ord(data)
   
def printResponse(rawVals):
  print "Raw:",
  
def TI_UUID(val):
  return UUID("%08X-0451-4000-b000-000000000000" % (0xF0000000+val))  

ctrl_c = False
keys = 0

notifyHnd = 74
keyPressState = 73
  
service_uuid = TI_UUID(0xFFE0)

config_uuid = TI_UUID(0xAA72)
data_uuid = TI_UUID(0xAA71)

sensorOn  = struct.pack("B", 0x01)
sensorOff = struct.pack("B", 0x00)

notifyOn = struct.pack("BB", 0x01, 0x00)
notifyOff = struct.pack("BB", 0x00, 0x00)

if len(sys.argv) != 2:
  print "Fatal, must pass device address:", sys.argv[0], "<device address>"
  quit()

try:
  print "Info, trying to connect to:", sys.argv[1]
  p = Peripheral(sys.argv[1])
  print "Info, connected and turning notify and sensor on!"

  ch = p.getCharacteristics(uuid=config_uuid)[0]
  ch.write(sensorOn, withResponse=True)
  
  # With bluepy if you need to read or write a Descriptor you have to 
  # access it using Peripheral readCharacteristic or writeCharacteristic 
  # and the appropriate handle
  p.setDelegate( MyDelegate("keys") )
  p.writeCharacteristic(notifyHnd, notifyOn)

  while True:
    try:
      if p.waitForNotifications(1.0):
        # handleNotification() was called
        if keys & 0x01:
          print "Info, Right Button"
        if keys & 0x02:
          print "Info, Left Button"
        if keys & 0x04:
          print "Info, Reed Switch"
    
    except KeyboardInterrupt:
      print "exiting..."
      ctrl_c=True
      
except:
  if not ctrl_c:
    print "Fatal, unexpected error!"
    traceback.print_exc()
    raise
  
finally:
  if not ctrl_c: 
    p.writeCharacteristic(74, notifyOff)
    ch = p.getCharacteristics(uuid=config_uuid)[0]
    ch.write(sensorOff, withResponse=True)
    p.disconnect()
    quit()
  os._exit(0)
