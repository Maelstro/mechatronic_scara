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
int id, val1, val2, valZ, enc1, enc2, enc3;
hLegoSensor_simple ls(hSens6);
hSensors::Lego_Touch sensor(ls);
bool pressed = false;

// Regulatory
hPIDRegulator reg1, reg2, reg3;

void initReg() {
    reg1.setScale(1);
    reg1.setKP(100);
    reg1.setKI(0.05);
    reg1.setKD(1000);
    reg1.dtMs = 5;
    reg1.stableRange = 5;
    reg1.stableTimes = 1;
    reg2 = reg1;
    reg3 = reg1;
    hMot1.attachPositionRegulator(reg1);
    hMot3.attachPositionRegulator(reg2);
    hMot4.attachPositionRegulator(reg3);
}


int convert(char buf[], int num) {
    int val = 0;
    for(int i = 1; i < num; i++)val += (buf[i]-48)*pow(10, num-i-1);
    if(buf[0]=='-')val *= -1;
    //val = (buf[3]-48) + (buf[2]-48)*10 + (buf[1]-48)*100 + (buf[0]-48)*1000;
    return val;
}
void readBuffer(char buf[], int number) {
    int k = 0;
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
    hMot4.rotAbs(0,400,false, INFINITE);
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

void moveJoint() {
    clearBuffers();
    readBuffer(bufTheta, 5);
    readBuffer(bufGamma, 5);
    val1 = convert(bufTheta, 5);
    val2 = convert(bufGamma, 5);
    val1 *= -1;
    printf("Converted data - value 1: %d\n", val1);
    printf("Converted data - value 2: %d\n", val2);
    hMot1.rotAbs(val1, 200, false, INFINITE);
    hMot3.rotAbs(val2, 200, false, INFINITE);
    hMot1.waitDone();
    hMot3.waitDone();
    enc1 = hMot1.getEncoderCnt();
    enc2 = hMot3.getEncoderCnt();
    printf("ENC1 = %d\n", enc1);
    printf("ENC2 = %d\n", enc2);
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
        hMot1.rotAbs(val1, 350, false, INFINITE);
        hMot3.rotAbs(val2, 350, false, INFINITE);
        hMot1.waitDone();
        hMot3.waitDone();
    }
    enc1 = hMot1.getEncoderCnt();
    enc2 = hMot3.getEncoderCnt();
    printf("Motor 1 encoder value: %d\n", enc1);
    printf("Motor 2 encoder value: %d\n", enc2);
}

void sendEncoderValues () {
    printf("Motor 1 encoder value: %d\n", enc1);
    printf("Motor 2 encoder value: %d\n", enc2);
    printf("Motor 3 encoder value: %d\n", enc3);
}

void caseSelector(int funct) {
    switch (funct) {
        case 1:     // Złącza
            printf("Joints\n");
            moveJoint();
            break;
        case 2:     // Pen
            moveZ();
            break;
        case 3:     // Reset enkoderów
            resetEncoder();
            break;
        case 4:     // Wiele punktów
            printf("Case 4\n");
            readPoints();
            break;
        case 5:     // Sterowanie klawiszami - złącza
            break;
        case 6:     // Sterowanie klawiszami - XY
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
    initReg();
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
