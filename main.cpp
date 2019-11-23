//Version3

#include <hFramework.h>
//#include "hCloudClient.h"
#include <hMotor.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <cmath>
#include <hSensor.h>
#include <hSensors/Lego_Touch.h>

//Bufory
char bufID[1] = {0};
char bufTheta[5] = {0};
char bufGamma[5] = {0};
char bufZ[5] = {0};
char bufPos = 0;
int id, val1, val2, valZ, enc1, enc2, enc3, k;
hLegoSensor_simple ls(hSens6);
hSensors::Lego_Touch sensor(ls);
bool pressed = false;

int convert(char buf[], int num) {
    int val = 0;
    for(int i = 1; i < num; i++)val += (buf[i]-48)*pow(10, num-i-1);
    if(buf[0]=='-')val *= -1;
    return val;
}
void readBuffer(char buf[], int number) {
    k = 0;
    Serial.waitForData(INFINITE);
    while(Serial.available() > 0 && (k < number)){
        buf[k] = getchar();
        k++;
    }
}

void clearBuffers() {
    bufID[0]=0;
    for(int i=0;i<5;i++){
        bufTheta[i] = bufGamma[i] = bufZ[0] = 0;
    }
}

void resetEncoder () {
    hMot1.resetEncoderCnt();
    hMot3.resetEncoderCnt();
    hMot4.resetEncoderCnt();
    hMot1.rotAbs(0,400,false, INFINITE);
    hMot3.rotAbs(0,400,false, INFINITE);
    hMot4.rotAbs(0,400,true, INFINITE);
}

void initMotors() {
    hMot1.setEncoderPolarity(Polarity::Reversed);       //Motor nr 1 - przy podstawie
    hMot3.setEncoderPolarity(Polarity::Reversed);       //Motor nr 2 - człon nr 2
    hMot4.setEncoderPolarity(Polarity::Reversed);       //Motor nr 3 - oś Z
    resetEncoder();
}

void halt() {
    while(true){
        pressed = sensor.isPressed();
        if(pressed==true) {
            sys.reset();
        }
    }
}

void getAllEncoders() {
    enc1 = hMot1.getEncoderCnt();
    enc2 = hMot3.getEncoderCnt();
    printf("%d\n", enc1);
    printf("%d\n", enc2);
}

void moveJoint() {
    clearBuffers();
    readBuffer(bufTheta, 5);
    readBuffer(bufGamma, 5);
    val1 = convert(bufTheta, 5);
    val2 = convert(bufGamma, 5);
    val1 *= -1;
    printf("Converted data - value 1: %d\n", val1);
    printf("Converted data - value 2: %d\n", val2);
    hMot1.rotAbs(val1, 500, false, INFINITE);
    hMot3.rotAbs(val2, 500, false, INFINITE);
    hMot1.waitDone();
    hMot3.waitDone();
    getAllEncoders();
}

void moveZ () {
    readBuffer(bufZ, 5);
    valZ = convert(bufZ, 5);
    printf("Converted data - value 3: %d\n", valZ);
    hMot4.rotAbs(valZ, 400, false, INFINITE);
    hMot4.waitDone();
    enc3 = hMot4.getEncoderCnt();
}

void readPoints () {
    while(Serial.available() > 0) {
        readBuffer(bufTheta, 5);
        readBuffer(bufGamma, 5);
        val1 = convert(bufTheta, 5);
        val2 = convert(bufGamma, 5);
        val1 = val1 * -1;
        hMot1.rotAbs(val1, 500, false, INFINITE);
        hMot3.rotAbs(val2, 300, false, INFINITE);
        hMot1.waitDone();
        hMot3.waitDone();
    }
    getAllEncoders();
}

void sendEncoderValues () {
    printf("Motor 1 encoder value: %d\n", enc1);
    printf("Motor 2 encoder value: %d\n", enc2);
    printf("Motor 3 encoder value: %d\n", enc3);
}

void caseSelector(int funct) {
    switch (funct) {
        case 1:     // Złącza
            moveJoint();
            break;
        case 2:     // Pen
            moveZ();
            break;
        case 3:     // Reset enkoderów
            resetEncoder();
            break;
        case 4:     // Wiele punktów
            readPoints();
            break;
        case 5:     // Sterowanie klawiszami - złącza
            k = 0;
            while(true){
                bufPos = getchar();
                if(bufPos=='a')hMot1.rotRel(-10,700,false,INFINITE);        // Oś 1 - lewo
                else if(bufPos=='d')hMot1.rotRel(10,700,false,INFINITE);    // Oś 1 - prawo
                else if(bufPos=='z')hMot3.rotRel(10,700,false,INFINITE);    // Oś 2 - lewo
                else if(bufPos=='c')hMot3.rotRel(-10,700,false,INFINITE);   // Oś 2 - prawo
                else if(bufPos=='q')break;
                bufPos = 0;
            }
            break;
        // case 6:     // Sterowanie klawiszami - XY
        //     break;
        case 7:
            // Wyślij pozycję
            getAllEncoders();
            break;
        default:
            hLED3.on();
            hLED1.on();
            hLED2.on();       
            break;
    }
}

void mainTask() {
    initMotors();
    resetEncoder();
    while(true){
        hLED1.off();
        hLED2.off();
        hLED3.off();
        Serial.flushRx();
        readBuffer(bufID, 1);
        id = (bufID[0]-48);
        caseSelector(id);
        clearBuffers();
    }
}

int hMain() {
    sys.setLogDev(&Serial);
    sys.taskCreate(halt);
    sys.taskCreate(mainTask);
    return 0;
}
