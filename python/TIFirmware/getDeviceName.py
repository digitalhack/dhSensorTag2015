import sys
from bluepy.btle import UUID, Peripheral

temp_uuid = UUID(0x2A00)

if len(sys.argv) != 2:
  print "Fatal, must pass device address:", sys.argv[0], "<device address>"
  quit()

p = Peripheral(sys.argv[1])

try:
    ch = p.getCharacteristics(uuid=temp_uuid)[0]
    if (ch.supportsRead()):
            print ch.read()

finally:
    p.disconnect()
