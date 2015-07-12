#
# TI SimpleLink SensorTag 2015
# Date: 2015 07 06
#
# Sensor: Humidity Temperature
# Values: Temperature and Humidity
#
import struct, sys, traceback
from bluepy.btle import UUID, Peripheral, BTLEException

def TI_UUID(val):
    return UUID("%08X-0451-4000-b000-000000000000" % (0xF0000000+val))

config_uuid = TI_UUID(0xAA22)
data_uuid = TI_UUID(0xAA21)

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
    
    # IR Temperature sensor returns 4 bytes object(LSB),
    # object(MSB), ambient(LSB) and ambient(MSB).
    # Python unpack using "<" which denotes little-endian format
    # and "hh" which denotes 2 unsigned short (2 byte/16 bit) values.
    rawVals=ch.read()
    #(tempVal, humidVal) = struct.unpack('<HH', ch.read())
    tempVal = (ord(rawVals[1])<<8)+ord(rawVals[0])
    humidVal = (ord(rawVals[3])<<8)+ord(rawVals[2])
    
    #object temp and ambient temp are calculated as shown below
    print "Temp: %.2f F" % float((tempVal / 65536.0 * 165 - 40) * 1.8 + 32)
    print "Humidity: %.2f %%RH" % float(humidVal / 65536.0 * 100)
    
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