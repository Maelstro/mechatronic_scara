//Odczyt kroków - serial port
#include <hFramework.h>
//#include "hCloudClient.h"
#include <hMotor.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>

using namespace hFramework;

char buffer1[1024] = {0xFF};
char buffer2[1024] = {0xFF};
int numBytes1, numBytes2, value1, value2, j=0;
int enc1, enc2;     //Enkodery

int hMain(){
    sys.setLogDev(&Serial);
    hLED1.off();     //Start programu
    hLED2.off();     //Wyłączenie diod

    hMot1.setEncoderPolarity(Polarity::Reversed);       //Motor nr 1 - przy podstawie
    hMot2.setEncoderPolarity(Polarity::Reversed);       //Motor nr 3 - oś Z
    hMot3.setEncoderPolarity(Polarity::Reversed);       //Motor nr 2 - człon nr 2

    while(true){
        Serial.flushRx();   //Czyszczenie buforu przed pierwszym uruchomieniem
        Serial.waitForData(INFINITE);
        while(Serial.available()>0){
            Serial.read(&buffer1[j], 1024, INFINITE);
            j++;
        }
        numBytes1 = j;
        j = 0;
        Serial.waitForData(INFINITE);
        while(Serial.available()>0){
            Serial.read(&buffer2[j], 1024, INFINITE);
            j++;
        }
        numBytes2 = j;
        j = 0;
        sys.delay(50);
        printf("Data read buffer 1: %s\n", buffer1);
         printf("Data read buffer 2: %s\n", buffer2);
        //Konwersja
        value1 = 0;
        for(int i = numBytes1 - 1; i >= 0;i--){
            value1 += static_cast<int>(buffer1[i]);
            if(i!=0)value1 = value1 << 8;
        }
        value2 = 0;
        for(int i = numBytes2 - 1; i >= 0;i--){
            value2 += static_cast<int>(buffer2[i]);
            if(i!=0)value2 = value2 << 8;
        }
        value1 = static_cast<int>(value1);
        value2 = static_cast<int>(value2);
        if(value1>32767)value1=value1-65536;
        if(value2>32767)value2=value2-65536;
        printf("Converted data - value 1: %d\n", value1);
        printf("Converted data - value 2: %d\n", value2);
        int pow2 = int((200*value2)/value1);
        hMot1.rotAbs(value1, 200, false, INFINITE);
        hMot3.rotAbs(value2, pow2, true, INFINITE);
        hMot1.waitDone();
        hMot3.waitDone();
        enc1 = hMot1.getEncoderCnt();
        enc2 = hMot3.getEncoderCnt();
        printf("Enc1 = %d, Enc2 = %d\n", enc1, enc2);
        sys.delay(200);
    }
}