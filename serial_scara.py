import serial, struct, time

ser = serial.Serial('/dev/ttyUSB0', 460800, parity=serial.PARITY_NONE, timeout=1)
print(ser.name)
ser.close()
ser.open()
while True:
    print("Write angles:")
    val1 = int(input("Angle 1: "))
    val2 = int(input("Angle 2: "))
    val3 = int(input("Linear movement: "))
    message = struct.pack('hhh', val1, val2, val3)
    print("Message to send: ", message)
    byteNum = ser.write(message)
    print(byteNum)
    while(True):
        resp = ""
        resp = ser.read_until()
        if(resp==None):
            break
        print(resp)
    print("Done")
    ser.reset_input_buffer()
