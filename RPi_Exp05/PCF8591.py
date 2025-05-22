import smbus
import time

class PCF8591:
  def __init__(self, address):
   self.address = address
   self.bus = smbus.SMBus(1)

  def read(self, channel):
   if channel in [0, 1, 2, 3]:
    self.bus.write_byte(self.address, 0x40 | channel)
    self.bus.read_byte(self.address)
    return self.bus.read_byte(self.address)
   return None

  def write(self, value):
   try:
    self.bus.write_byte_data(self.address, 0x40, int(value))
   except Exception as e:
    print(f"Error: Device address: 0x{self.address:02X}")
    print(e)

if __name__ == "__main__":
  adc = PCF8591(0x48)

  while True:
   value = adc.read(0)
   print(value)
   adc.write(value * (255 - 125) / 255 + 125)
   time.sleep(0.3)