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
#include <Lego_Touch.h>

using namespace hFramework;

char buffer1[2] = {0xFF};
char buffer2[2] = {0xFF};
char buffer3[2] = {0xFF};

int numBytes1, numBytes2, numBytes3, value1, value2, value3, j=0;
int enc1, enc2, enc3;     //Enkodery

int hMain(){
    hLegoSensor_simple ls(hSens6);
    hSensors::Lego_Touch sensor(ls);
    bool pressed;
    sys.setLogDev(&Serial);
    hLED1.off();     //Start programu
    hLED2.off();     //Wyłączenie diod
    hMot1.setEncoderPolarity(Polarity::Reversed);       //Motor nr 1 - przy podstawie
    hMot3.setEncoderPolarity(Polarity::Reversed);       //Motor nr 2 - człon nr 2
    hMot4.setEncoderPolarity(Polarity::Reversed);       //Motor nr 3 - oś Z
    IServo &servo = hMot1.useAsServo();
    servo.calibrate(-1800,700, 1800, 1500);

    while(true){
        Serial.flushRx();   //Czyszczenie buforu przed pierwszym uruchomieniem
        Serial.waitForData(INFINITE);
        while(Serial.available()>0){
            Serial.read(&buffer1[j], sizeof(buffer1), INFINITE);
            j++;
        }
        numBytes1 = j;
        j = 0;
        Serial.waitForData(INFINITE);
        while(Serial.available()>0){
            Serial.read(&buffer2[j], sizeof(buffer2), INFINITE);
            j++;
        }
        numBytes2 = j;
        j = 0;
        Serial.waitForData(INFINITE);
        while(Serial.available()>0){
            Serial.read(&buffer3[j], sizeof(buffer3), INFINITE);
            j++;
        }
        Serial.flushRx();
        numBytes3 = j;
        j = 0;
        sys.delay(50);
        printf("Data read buffer 1: %s", buffer1);
        printf("Data read buffer 2: %s", buffer2);
        printf("Data read buffer 3: %s", buffer3);
        //Konwersja
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
        printf("Converted data - value 1: %d", value1);
        printf("Converted data - value 2: %d", value2);
        printf("Converted data - value 3: %d", value3);
        if(value1<1500 && value2<1500 && value3<1000){
            hMot1.rotAbs(value1, 200, false, INFINITE);
            hMot3.rotAbs(value2, 200, false, INFINITE);
            hMot4.rotAbs(value3);
            printf("Moving");
        }
        hMot1.waitDone();
        hMot3.waitDone();
        hMot4.waitDone();
        sys.delay(200);
        enc1 = hMot1.getEncoderCnt();
        enc2 = hMot3.getEncoderCnt();
        enc3 = hMot4.getEncoderCnt();
        hMot1.stop();
        hMot3.stop();
        hMot4.stop();
        printf("Enc1 = %d, Enc2 = %d, Enc3 = %d", enc1, enc2, enc3);
        sys.delay(200);
    }
}