import serial, struct, time

ser = serial.Serial()
ser.baudrate = 460800
ser.port = 'COM6'
ser.open()
data = struct.pack('<hhh', 100, 100, 100) 
print(data)
ser.write(data)
while True:
    time.sleep(1)
    print(ser.read_until())
ser.close()
