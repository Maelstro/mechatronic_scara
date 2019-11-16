import serial, struct

with serial.Serial() as ser:
    ser.baudrate = 460800
    ser.port = 'COM6'
    ser.open()
    data = struct.pack('i', 100) 
    print(data, data)
    ser.write(data)
    ser.write(data)
