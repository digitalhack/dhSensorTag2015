#
# TI SimpleLink SensorTag 2015
# Date: 2015 07 06
#
# Sensor: Barometer
# Values: Temperature and Pressure
# Note: As of Jul 6 2015 the barometer sensor reading in the Android App Rev 2.20 Beta
# isn't reported correctly
#
import struct, sys, traceback, time
from bluepy.btle import UUID, Peripheral, BTLEException

def TI_UUID(val):
    return UUID("%08X-0451-4000-b000-000000000000" % (0xF0000000+val))

config_uuid = TI_UUID(0xAA42)
data_uuid = TI_UUID(0xAA41)

sensorOn  = struct.pack("B", 0x01)
sensorOff = struct.pack("B", 0x00)

if len(sys.argv) != 2:
  print "Fatal, must pass device address:", sys.argv[0], "<device address>"
  quit()

try:
  print "Info, trying to connect to:", sys.argv[1]
  p = Peripheral(sys.argv[1])

except BTLEException:
  print "Fatal, unable to connect!"
  
except:
  print "Fatal, unexpected error!"
  traceback.print_exc()
  raise

else:

  try:
    print "Info, connected and turning sensor on!"
    ch = p.getCharacteristics(uuid=config_uuid)[0]
    ch.write(sensorOn, withResponse=True)
    
    print "Info, reading values!"
    ch = p.getCharacteristics(uuid=data_uuid)[0]
    
    # The barometer sensor returns 6 bytes: rawTemp(LowByte), rawTemp(MiddleByte),
    # rawTemp(HighByte), rawPressure(LowByte), rawPressure(MiddleByte) and 
    # rawPressure(HighByte).  Temp and Pressure are calculated by dividing 
    # rawTemp / 100 F and rawPressure / 100 hPa.
    # With software v1.12 this program and the iOS app report the same pressure but
    # the Android app reports about 12 to 13 hPa lower.

    for i in range (0, 9):
      rawVals = ch.read()
      print "Raw:",
      for rawVal in rawVals:
        temp = ord(rawVal)
        print "%2.2x" % temp,
      print 
      print "Temp: %.2f F" % float(((ord(rawVals[2])<<16)+
        (ord(rawVals[1])<<8)+ord(rawVals[0]))/100.0 * 1.8 + 32)
      print "Pressure: %.4f hPa" % float(((ord(rawVals[5])<<16)+
        (ord(rawVals[4])<<8)+ord(rawVals[3]))/100.0) # * 0.02952998751)
      time.sleep(1)
    
    print "Info, turning sensor off!"
    ch = p.getCharacteristics(uuid=config_uuid)[0]
    ch.write(sensorOff, withResponse=True)
    
  except:
    print "Fatal, unexpected error!"
    traceback.print_exc()
    raise

  finally:
    print "Info, disconnecting!"
    p.disconnect()
    
finally:
  quit()