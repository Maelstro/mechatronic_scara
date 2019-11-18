#include <hFramework.h>
//#include "hCloudClient.h"
#include <hMotor.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <cmath>
#include <vector>


using namespace hFramework;
char func_id;
// char inp1[256] = {0};
// char inp2[256] = {0};
int inp1 = 0, inp2 = 0;
std::vector<char> buffer;
std::vector<char> buffer2;
int theta_a, theta_b, enc1, enc2, i;

void hMain()
{
	sys.setLogDev(&Serial);		//Serial initialization
	
	hLED1.off();
	hLED2.on();
	hMot1.setEncoderPolarity(Polarity::Reversed);		//Set polarization
	hMot2.setEncoderPolarity(Polarity::Reversed);
	hMot3.setEncoderPolarity(Polarity::Reversed);
	Serial.flushRx();
	while(1){
		buffer.clear();
		buffer2.clear();
		hLED1.on();
		hLED2.off();
		Serial.waitForData(INFINITE);
		for(int i=0; i<3;i++){
			char c = getchar();
			buffer.push_back(c);
			printf("%c", c);
		}
		theta_a = atoi(&buffer[0])*100 + atoi(&buffer[1])*10 + atoi(&buffer[2]);
		buffer.clear();
		Serial.flushRx();
		sys.delay(0.01);
		for(int j=0; j<3;j++){
			char c = getchar();
			buffer.push_back(c);
			printf("%c", c);
		}
		theta_b = atoi(&buffer[0])*100 + atoi(&buffer[1])*10 + atoi(&buffer[2]);
		// i = 0;
		// while(Serial.available()>0){
		// 	inp1[i] = getchar();
		// 	if(inp1[i]=='\n')break;
		// 	i++;
		// }
		// int size_inp1 = i;
		// i = 0;
		// while(Serial.available()>0){
		// 	inp2[i] = getchar();
		// 	if(inp2[i]=='\n')break;
		// 	i++;
		// }
		// int size_inp2 = i;
		// i = 0;
		//Serial.write(&inp1, sizeof(inp1), INFINITE);
		//Serial.write(&inp2, sizeof(inp2), INFINITE);
		// char tmp1[size_inp1];
		// char tmp2[size_inp2];
		// for(int j=0;j<size_inp1; j++)tmp1[j]=inp1[j];
		// for(int j=0;j<size_inp2; j++)tmp2[j]=inp2[j];
		// printf("%s\n", inp1);
		// printf("%d\n", inp2);
		// int i = 0;
		// while(true){
		// 	if(inp1[i]=='\n')break;
		// 	else i+=1;
		// }
		// int size_inp1 = i;
		// if(inp1[0]=='-')theta_a*=-1;
		// while(i>=0){
		// 	if(i==0 && theta_a<0)break;
		// 	theta_a += ((int(inp1[i])-48)*pow(10, (size_inp1-i-1)));
		// 	i-=1;
		// }
		// i = 0;
		// while(true){
		// 	if(inp2[i]=='\n')break;
		// 	else i+=1;
		// }
		// int size_inp2 = i;
		// if(inp2[0]=='-')theta_b*=-1;
		// while(inp2[i]!='\n'){
		// 	if(i==0 && theta_b<0)break;
		// 	theta_b += ((int(inp2[i])-48)*pow(10, (size_inp2-i-1)));
		// 	i-=1;
		// }
		// theta_a = atoi(tmp1);
		// theta_b = atoi(tmp2);
		//printf("%d", theta_a);
		//printf("%d", theta_b);
		if(theta_a<1500 && theta_b<1500){
			hMot1.rotAbs(theta_a, 200, false, INFINITE);
			hMot3.rotAbs(theta_a, 200, true, INFINITE);
		}
		
		printf("Decoded theta_a: %d\n", theta_a);
		printf("Decoded theta_b: %d\n", theta_b);
		sys.delay(50);
		enc1 = hMot1.getEncoderCnt();
		enc2 = hMot3.getEncoderCnt();
		// printf("Position changed by %f, %f\n", theta_a, theta_b);
		// printf("Encoder of M1: %f\n", enc1);
		// printf("Encoder of M2: %f\n", enc2);
		Serial.flushRx();
		hLED1.off();
		hLED2.on();
		sys.delay_ms(200);
	}
}
