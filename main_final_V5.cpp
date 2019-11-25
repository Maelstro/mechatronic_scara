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

// Definicja zmiennych - trochę tego jest
// Bufory
char bufID[1] = {0};
char bufTheta[5] = {0};
char bufGamma[5] = {0};
char bufZ[5] = {0};
char bufPos = 0;
char bufX[5] = {0};
char bufY[5] = {0};

// Zmienne bardziej numeryczne niż znaki ASCII
int id, val1, val2, valZ, enc1, enc2, enc3, k;
hLegoSensor_simple ls(hSens6);
hSensors::Lego_Touch sensor(ls);
bool pressed = false;
int penDown = 590;                      // Parametr określający, kiedy pisak jest dociśnięty do kartki
float arm_1 = 137.5;                    // Długość członu 1
float arm_2 = 90.0;                     // Długość członu 2
float offset = 40.0;                    // Offset od osi 1 do początku kartki, punktu (0,0)
float D;                                // Parametr do obliczeń
double gamma2, theta;                   // Kąty, theta = kąt 1, gamma = kąt 2
int point_num = 1;
float currentX, currentY;               // Obecne położenie X-Y, potrzebne do ruchu w trybie manualnym
float posX1, posY1, posX2, posY2, r;
bool isCalculated = false;

// Regulator PID - próby dostrojenia (?)
hPIDRegulator reg1, reg2, reg3;

void initRegulator() {      // Inicjalizacja parametrów regulatora PID do silników
    reg1.setScale(1);
    reg1.setKP(30.0);
    reg1.setKI(0.1);
    reg1.setKD(1000);
    reg1.dtMs = 3;
    reg1.stableRange = 10;
    reg1.stableTimes = 3;
    reg2 = reg1;
    reg3 = reg1;
    hMot1.attachPositionRegulator(reg1);
    hMot3.attachPositionRegulator(reg2);
    hMot4.attachPositionRegulator(reg3);
}

// Sterowanie X-Y

void angleToStep() {        // Konwersja z wartości kątów na kroki silnika
    if(theta<0 || theta>180)printf("Theta out of range: %f\n", theta);
    if(gamma2< (-120) || gamma2>120)printf("Gamma out of range: %f\n", theta);
    else {
        val1 = int(14*theta)*-1;
        val2 = int((28.0/3.0)*gamma2);
    }
}

void convertCartesian(float pos_x, float pos_y) {       // Konwersja współrzędnych kartezjańskich na kroki silnika
    if(pos_x<0)pos_x-=10;
    if(pos_x>0)pos_x+=10;
    if(abs(pos_x)>100)printf("Position X out of range: %d\n", pos_x);
    if((pos_y>200) || (pos_y<0))printf("Position Y out of range: %d\n", pos_y);
    else {
        if(pos_x<=0)pos_x+=10;
        pos_y += offset;
        D = (pos_x*pos_x + pos_y*pos_y - arm_1*arm_1 - arm_2*arm_2)/(2*arm_1*arm_2);
        gamma2 = atan2(-sqrt(1-D*D), D);
        theta = atan2(pos_y, pos_x) - atan2((arm_2*sin(gamma2)), (arm_1+arm_2*cos(gamma2)));
        gamma2= gamma2*180/M_PI;
        theta = theta*180/M_PI;
        printf("Theta: %f\n", theta);
        printf("Gamma: %f\n", gamma2);
        angleToStep();
        printf("Kroki Val1: %f\n", val1);
        printf("Kroki Val2: %f\n", val2);
        hMot1.rotAbs(val1, 500, false, INFINITE);
        hMot3.rotAbs(val2, 500, false, INFINITE);
        sys.delay_ms(500);
    }
}

// Obliczanie trajektorii
// 1. Linia prosta + prostokąt
// 2. Okrąg
// 3. Okrąg w kwadrat wpisany

void trajectoryLine(float x1, float y1, float x2, float y2, int num) {      // Rysowanie linii
    float a, b, x_diff, y_diff, x_tmp;                                      // 2 punkty -> dzielenie prostej na 'num' punktów
    if((x1-x2)==0) {
        if(y1 != y2){
            y_diff = (y2-y1)/num;
            for(int i = 0; i <= num; i++){
                if(i!=0)y1 += y_diff;
                printf("Punkt nr %d\n",point_num++);
                printf("X,Y : %f, %f\n", x1, y1);
                convertCartesian(x1, y1);                                   // Przemieszczanie się do danego punktu
            }
        }
    }
    else {
        a = float(y1 - y2)/float(x1-x2);
        b = (y1 - a*x1);
        x_diff = (x2-x1)/num;
        for(int i = 0; i < num; i++){
            if(i!=0)x1 += x_diff;
            printf("Punkt nr %d\n",point_num++);
            printf("X,Y : %f, %f\n", x1, y1);
            convertCartesian(x1, (a*x1 + b));
        }
    }
}

void trajectoryRect(float x1, float y1, float x2, float y2, int num_1side) {    // Rysowanie prostokąta
    convertCartesian(x1, y1);       // Przemieszczenie się do punktu pierwszego
    hMot1.waitDone();               // Oczekiwanie na koniec ruchu
    hMot3.waitDone();
    sys.delay_ms(500);
    hMot4.rotAbs(penDown, 500, true, INFINITE);         // Opuszczenie pisaka
    sys.delay_ms(500);
    trajectoryLine(x1, y1, x2, y1, num_1side);          // Początek rysowania linii
    trajectoryLine(x2, y1, x2, y2, int(num_1side/2));
    trajectoryLine(x2, y2, x1, y2, num_1side);
    trajectoryLine(x1, y2, x1, y1, int(num_1side/2));
    hMot1.waitDone();
    hMot3.waitDone();
    sys.delay_ms(500);
    hMot4.rotAbs(0, 700, true, INFINITE);               // Podniesienie pisaka
    printf("Finished drawing a rectangle.\n");
}

void trajectoryCircle(float r, float x, float y, int num) {     // Rysowanie okręgu - obliczenia dobre, jakość ruchu zła
    float pos_X, pos_Y;
    pos_X = pos_Y = 0;
    for (int i=1; i <=num; i++){
        pos_X = float(cos(2*M_PI/num*i)*r);
        pos_Y = float(sin(2*M_PI/num*i)*r);
        pos_X += x;
        pos_Y += y;
        printf("Okrąg - Punkt nr %d", point_num);
        printf("X,Y : %f, %f\n", pos_X, pos_Y);
        convertCartesian(pos_X, pos_Y);
        if(i == 1) {
            sys.delay_ms(500);
            hMot4.rotAbs(penDown, 700, true, INFINITE);
            sys.delay_ms(500);
        }
    }
    hMot1.waitDone();
    hMot3.waitDone();
    hMot4.rotAbs(0, 700, true, INFINITE);
    sys.delay_ms(500);
    printf("Finished drawing a circle.\n");
}

void CircleInASquare(float x1, float y1, float x2, float y2, int num_sq, int num_circle) {      // Okrąg wpisany w prostokąt
    trajectoryRect(x1, y1, x2, y2, num_sq);                                                     // Analogicznie do ruchu po okręgu, bardzo zła jakość rysowania okręgu
    float radius = float(abs(x2-x1)/2);
    sys.delay_ms(500);
    if(x2>x1 && y2>y1)trajectoryCircle(radius, x1+radius, y1+radius, num_circle);
    if(x2<x1 && y2>y1)trajectoryCircle(radius, x2+radius, y1+radius, num_circle);
    if(x2>x1 && y2<y1)trajectoryCircle(radius, x1+radius, y2+radius, num_circle);
    if(x2<x1 && y2<y1)trajectoryCircle(radius, x2+radius, y2+radius, num_circle);
    hMot1.waitDone();
    hMot3.waitDone();
    printf("Finished drawing.\n");
    
}

// Sterowanie XY - tryb ręczny

void StepToCartesian() {        // Konwersja z pozycji silników na współrzędne kartezjańskie z uwzględnieniem offsetu na osi Y
    val1 = hMot1.getEncoderCnt();
    val2 = hMot3.getEncoderCnt();
    theta = ((-1*val1)/14.0)*(M_PI/180);
    gamma2 = ((val2)/(28.0/3.0))*(M_PI/180);
    printf("Theta, gammma: %f, %f\n", theta, gamma2);
    currentX = (arm_1*cos(theta)+arm_2*cos(theta+gamma2));
    currentY = (arm_1*sin(theta)+arm_2*sin(theta+gamma2)) - offset;
    isCalculated = true;        // Pozycja przeliczana jest tylko raz
}

void Y_Up() {       // Ruch do przodu wzdłuż osi Y
    if(isCalculated==false)StepToCartesian();
    printf("Current XY: %f, %f\n", currentX, currentY);
    currentY = currentY + 5.0;
    convertCartesian(currentX, currentY);
}

void Y_Down() {     // Ruch do tyłu wzdłuż osi Y
    if(isCalculated==false)StepToCartesian();
    printf("Current XY: %f, %f\n", currentX, currentY);
    currentY = currentY - 5.0;
    convertCartesian(currentX, currentY);
}

void X_Left() {     // Ruch w lewo wzdłuż osi X
    if(isCalculated==false)StepToCartesian();
    printf("Current XY: %f, %f\n", currentX, currentY);
    currentX = currentX - 5.0;
    convertCartesian(currentX, currentY);
}

void X_Right() {    // Ruch w prawo wzdłuż osi X
    if(isCalculated)StepToCartesian();
    printf("Current XY: %f, %f\n", currentX, currentY);
    currentX = currentX + 5.0;
    convertCartesian(currentX, currentY);
}

int convert(char buf[], int num) {      // Konwersja wartości odczytanej na porcie szeregowym
    int val = 0;
    for(int i = 1; i < num; i++)val += (buf[i]-48)*pow(10, num-i-1);
    if(buf[0]=='-')val *= -1;
    return val;
}
void readBuffer(char buf[], int number) {       // Odczyt bufora, 'number' znaków
    k = 0;
    Serial.waitForData(INFINITE);
    while(Serial.available() > 0 && (k < number)){
        buf[k] = getchar();
        k++;
    }
}

void clearBuffers() {       // Czyszczenie bufora
    bufID[0]=0;
    for(int i=0;i<5;i++){
        bufTheta[i] = bufGamma[i] = bufZ[0] = 0;
    }
}

void resetEncoder () {      // Reset enkoderów
    hMot1.resetEncoderCnt();
    hMot3.resetEncoderCnt();
    hMot4.resetEncoderCnt();
    hMot1.rotAbs(0,400,false, INFINITE);        // Upewnienie się, że silniki nie poruszają się
    hMot3.rotAbs(0,400,false, INFINITE);
    hMot4.rotAbs(0,400,false, INFINITE);
    hMot1.waitDone();
    hMot3.waitDone();
    hMot4.waitDone();
}

void initMotors() {
    hMot1.setEncoderPolarity(Polarity::Reversed);       // Motor nr 1 - przy podstawie
    hMot3.setEncoderPolarity(Polarity::Reversed);       // Motor nr 2 - człon nr 2
    hMot4.setEncoderPolarity(Polarity::Reversed);       // Motor nr 3 - oś Z
    resetEncoder();
}

void halt() {       // Stop awaryjny
    while(true){
        pressed = sensor.isPressed();
        if(pressed==true) {
            sys.reset();
        }
    }
}

void getAllEncoders() {         // Odczyt wartości z enkoderów
    enc1 = hMot1.getEncoderCnt();
    enc2 = hMot3.getEncoderCnt();
    enc3 = hMot4.getEncoderCnt();
    printf("%d\n", enc1);
    printf("%d\n", enc2);
    printf("%d\n", enc3);
}

void moveJoint() {      // Ruch we współrzędnych złączowych, wejście - ilość kroków
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

void moveZ () {         // Ruch pisakiem góra-dół
    readBuffer(bufZ, 5);
    valZ = convert(bufZ, 5);
    printf("Converted data - value 3: %d\n", valZ);
    hMot4.rotAbs(valZ, 400, false, INFINITE);
    hMot4.waitDone();
    enc3 = hMot4.getEncoderCnt();
}

void readPoints () {    // Ruch do wielu punktów, obecnie nieużywane
    while(Serial.available() > 0) {
        readBuffer(bufTheta, 5);
        readBuffer(bufGamma, 5);
        val1 = convert(bufTheta, 5);
        val2 = convert(bufGamma, 5);
        val1 = val1 * -1;
        hMot1.rotAbs(val1, 500, false, INFINITE);
        hMot3.rotAbs(val2, 500, false, INFINITE);
        hMot1.waitDone();
        hMot3.waitDone();
    }
    sys.delay_ms(500);
    hMot4.rotAbs(0,500,true,INFINITE);
    getAllEncoders();
    printf("%d\n");
}

void sendEncoderValues () {     // Wysłanie wartości z enkoderów
    printf("Motor 1 encoder value: %d\n", enc1);
    printf("Motor 2 encoder value: %d\n", enc2);
    printf("Motor 3 encoder value: %d\n", enc3);
}

void caseSelector(int funct) {      // Wybór funkcji do wykonania dla podanego ID
    switch (funct) {
        case 0:     // do punktu XY
            readBuffer(bufX, 5);
            readBuffer(bufY, 5);
            posX1 = convert(bufX, 5);
            posY1 = convert(bufY, 5);
            printf("PosX, PosY: %f, %f\n", posX1, posY1);
            convertCartesian(posX1, posY1);
            break;
        case 1:     // Złącza
            moveJoint();
            break;
        case 2:     // Pen
            moveZ();
            break;
        case 3:     // Reset enkoderów
            resetEncoder();
            break;
        case 4:     // Wiele punktów - prostokąt
            readBuffer(bufX, 5);
            readBuffer(bufY, 5);
            posX1 = convert(bufX, 5);
            posY1 = convert(bufY, 5);
            readBuffer(bufX, 5);
            readBuffer(bufY, 5);
            posX2 = convert(bufX, 5);
            posY2 = convert(bufY, 5);
            if(posX1==posX2 || posY1==posY2) {
                convertCartesian(posX1, posY1);
                sys.delay_ms(2000);
                hMot4.rotAbs(penDown, 700, true, INFINITE);
                sys.delay_ms(500);
                trajectoryLine(posX1, posY1, posX2, posY2, 30);
                hMot4.rotAbs(0, 700, true, INFINITE);
            }
            else trajectoryRect(posX1, posY1, posX2, posY2, 30);
            // readPoints();
            break;
        case 5:     // Sterowanie klawiszami - złącza
            k = 0;
            while(true){
                bufPos = getchar();
                if(bufPos=='a')hMot1.rotRel(-10,500,false,INFINITE);        // Oś 1 - lewo
                else if(bufPos=='d')hMot1.rotRel(10,500,false,INFINITE);    // Oś 1 - prawo
                else if(bufPos=='z')hMot3.rotRel(10,500,false,INFINITE);    // Oś 2 - lewo
                else if(bufPos=='c')hMot3.rotRel(-10,500,false,INFINITE);   // Oś 2 - prawo
                else if(bufPos=='w')hMot4.rotRel(-5,500,false,INFINITE);    // Oś 3 - góra
                else if(bufPos=='s')hMot4.rotRel(5,500,false,INFINITE);     // Oś 3 - dół
                else if(bufPos=='q')break;
                bufPos = 0;
            }
            break;
        case 6:     // Sterowanie klawiszami - XY
            isCalculated = false;
            while(true){
                bufPos = getchar();
                if(bufPos=='w')Y_Up();
                else if(bufPos=='s')Y_Down();
                else if(bufPos=='a')X_Left();
                else if(bufPos=='d')X_Right();
                else if(bufPos=='q')break;
                bufPos = 0;
            }
            break;
        case 7:     // Wyślij pozycję
            getAllEncoders();
            break;
        case 8:     // Rysuj okrąg
            readBuffer(bufZ, 5);
            readBuffer(bufX, 5);
            readBuffer(bufY, 5);
            r = convert(bufZ, 5);
            posX1 = convert(bufX, 5);
            posY1 = convert(bufY, 5);
            trajectoryCircle(r, posX1, posY1, 360);
            break;
        case 9:      // Rysuj okrąg w prostokącie
            readBuffer(bufX, 5);
            readBuffer(bufY, 5);
            posX1 = convert(bufX, 5);
            posY1 = convert(bufY, 5);
            readBuffer(bufX, 5);
            readBuffer(bufY, 5);
            posX2 = convert(bufX, 5);
            posY2 = convert(bufY, 5);
            CircleInASquare(posX1, posY1, posX2, posY2, 10, 100);
            break;
        default:
            hLED3.on();
            hLED1.on();
            hLED2.on();       
            break;
    }
}

void mainTask() {       // Główny task wykonywany przez program
    initMotors();       // Inicjalizacja parametrów pracy silników
    resetEncoder();     // Reset enkoderów
    initRegulator();    // Inicjalizacja regulatorów
    while(true){
        hLED1.off();
        hLED2.off();
        hLED3.off();
        Serial.flushRx();   // Czyszczenie bufora ze śmieci
        readBuffer(bufID, 1);   // Odczyt ID funkcji
        id = (bufID[0]-48);     // Zdekodowanie odczytanego ID
        caseSelector(id);       // Wybór funkcji do działania
        clearBuffers();         // Czyszczenie buforów
    }
}

int hMain() {
    sys.setLogDev(&Serial);     // Wyjście na port szeregowy
    sys.taskCreate(halt);       // Utworzenie wątku z E-Stopem
    sys.taskCreate(mainTask);   // Utworzenie wątku z funkcją główną
    return 0;
}
