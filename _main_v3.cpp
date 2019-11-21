//Odczyt kroków - serial port
#include <hFramework.h>
//#include "hCloudClient.h"
#include <hMotor.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <thread>
#include <hSensor.h>
#include <hSensors/Lego_Touch.h>

using namespace hFramework;

char buffer1[2] = {0xFF};
char buffer2[2] = {0xFF};
char buffer3[2] = {0xFF};
char bufferTotal[6] = {0};

hLegoSensor_simple ls(hSens6);
hSensors::Lego_Touch sensor(ls);
bool pressed = false;

int numBytes1, numBytes2, numBytes3, value1, value2, value3, j=0;
int enc1, enc2, enc3, number;     //Enkodery

void halt() {
    while(true){
        pressed = sensor.isPressed();
        if(pressed==true) {
            hMot1.setPower(0);
            hMot3.setPower(0);
            hMot4.setPower(0);
            hMot1.waitDone();
            hMot3.waitDone();
            hMot4.waitDone();
            sys.reset();
        }
    }
}

void checkSerial() {
    if(numBytes1 == 0)buffer1[0] = buffer1[1] = 0;
    if(numBytes2 == 0)buffer2[0] = buffer2[1] = 0;
    if(numBytes3 == 0)buffer3[0] = buffer3[1] = 0;
}

void initMotors() {
    hMot1.setEncoderPolarity(Polarity::Reversed);       //Motor nr 1 - przy podstawie
    hMot3.setEncoderPolarity(Polarity::Reversed);       //Motor nr 2 - człon nr 2
    hMot4.setEncoderPolarity(Polarity::Reversed);       //Motor nr 3 - oś Z
}

void readSingleSerial() {
    Serial.flushRx();
    number = Serial.waitForData(INFINITE);
    Serial.read(bufferTotal, sizeof(bufferTotal), INFINITE);
}

void convertShort(){
    value1 = 0;
    for(int i = 1; i >= 0;i--){ 
        value1 += static_cast<int>(buffer1[i]);
        if(i!=0)value1 = value1 << 8;
    }
    value2 = 0;
    for(int i = 3; i >= 2;i--){
        value2 += static_cast<int>(buffer2[i]);
        if(i!=0)value2 = value2 << 8;
    }
    value3 = 0;
    for(int i = 5; i >= 4;i--){
        value3 += static_cast<int>(buffer3[i]);
        if(i!=0)value3 = value3 << 8;
    }
    if(value1>32767)value1=value1-65536;
    if(value2>32767)value2=value2-65536;
    if(value3>32767)value3=value3-65536;
    printf("Converted data - value 1: %d\n", value1);
    printf("Converted data - value 2: %d\n", value2);
    printf("Converted data - value 3: %d\n", value3);
}

void readSerial() {
    Serial.flushRx();   //Czyszczenie buforu przed pierwszym uruchomieniem
    Serial.waitForData(INFINITE);
    while(Serial.available()>0 && (j<2)){
        Serial.read(&buffer1[j], sizeof(buffer1), 1);
        j++;
    }
    numBytes1 = j;
    j = 0;
    printf("Bytes read - buf 1: %d\n", numBytes1);
    Serial.waitForData(INFINITE);
    while(Serial.available()>0 && (j<2)){
        Serial.read(&buffer2[j], sizeof(buffer2), 1);
        j++;
    }
    numBytes2 = j;
    j = 0;
    printf("Bytes read - buf 2: %d\n", numBytes2);
    Serial.waitForData(INFINITE);
    while(Serial.available()>0 && (j<2)){
        Serial.read(&buffer3[j], sizeof(buffer3), 1);
        j++;
    }
    numBytes3 = j;
    j = 0;
    printf("Bytes read - buf 3: %d\n", numBytes3);
    sys.delay(50);
    printf("Data read buffer 1: %s\n", buffer1);
    printf("Data read buffer 2: %s\n", buffer2);
    printf("Data read buffer 3: %s\n", buffer3);
}

void convertValue() {
    value1 = 0;
    for(int i = 1; i >= 0;i--){ 
        value1 += static_cast<int>(buffer1[i]);
        if(i!=0)value1 = value1 << 8;
    }
    value2 = 0;
    for(int i = 1; i >= 0;i--){
        value2 += static_cast<int>(buffer2[i]);
        if(i!=0)value2 = value2 << 8;
    }
    value3 = 0;
    for(int i = 1; i >= 0;i--){
        value3 += static_cast<int>(buffer3[i]);
        if(i!=0)value3 = value3 << 8;
    }
    if(value1>32767)value1=value1-65536;
    if(value2>32767)value2=value2-65536;
    if(value3>32767)value3=value3-65536;
    printf("Converted data - value 1: %d\n", value1);
    printf("Converted data - value 2: %d\n", value2);
    printf("Converted data - value 3: %d\n", value3);
}

void workFlow() {
    sys.setLogDev(&Serial);
    hLED1.off();     //Start programu
    hLED2.off();     //Wyłączenie diod
    initMotors();

    while(true){
        readSingleSerial();
        printf("Number read: %d\n", number);
        //checkSerial();
        //convertValue();
        convertShort();        
        if(value1<1500 && value2<1500 && value3<1000){
            hMot1.rotAbs(value1, 300, false, INFINITE);
            hMot3.rotAbs(value2, 300, false, INFINITE);
            hMot4.rotAbs(value3, 700, false, INFINITE);
            printf("Moving\n");
        }
        hMot1.waitDone();
        hMot4.waitDone();
        hMot3.waitDone();
        sys.delay(200);
        enc1 = hMot1.getEncoderCnt();
        enc2 = hMot3.getEncoderCnt();
        enc3 = hMot4.getEncoderCnt();
        hMot1.stop();
        hMot3.stop();
        hMot4.stop();
        printf("Enc1 = %d, Enc2 = %d, Enc3 = %d\n", enc1, enc2, enc3);
        sys.delay(200);
    }
}

int hMain() {
    hTask t2 = sys.taskCreate(halt);
    hTask t1 = sys.taskCreate(workFlow);
    t2.join();
    t1.join();
    return 0;
}