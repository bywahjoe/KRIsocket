#include "Wire.h"
#include "I2Cdev.h"
#include "HMC5883L.h"
#include <Encoder.h>

#include <LiquidCrystal_I2C.h>

#define greenECR 3
#define whiteECR 2
#define greenECL 19
#define whiteECL 18

#define encoder0PinA 3 //R
#define encoder0PinB 2 

#define encoder1PinA 18
#define encoder1PinB 19

Encoder mLeft(19, 18);
Encoder mRight(3, 2);

LiquidCrystal_I2C lcd(0x27, 16, 2);
HMC5883L mag;

int16_t mx, my, mz;
int majuR=2400;
long pulseL=0,pulseR=0;
//int mundurR=1100;
//volatile long pulseL=0,pulseR=0;

volatile long encoder0Pos = 0; //
volatile long encoder1Pos = 0;
unsigned now,before;
typedef struct 
{
  int32_t kompas;
  int32_t rotationL;
  int32_t rotationR;
  long vpulseL;
  long vpulseR;    
} mylog;

mylog go;
void setup() {
  Wire.begin();
  Serial.begin(9600);
//  Serial.println("OK");
  mag.initialize();

//  pinMode(greenECR, INPUT_PULLUP);
//  pinMode(whiteECR, INPUT_PULLUP);
//  pinMode(greenECL, INPUT_PULLUP);
//  pinMode(whiteECL, INPUT_PULLUP);
  
//  pinMode(encoder0PinA, INPUT_PULLUP);
//  pinMode(encoder0PinB, INPUT_PULLUP);
//  pinMode(encoder1PinA, INPUT_PULLUP);
//  pinMode(encoder1PinB, INPUT_PULLUP);
//  attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoderA, CHANGE);
//  attachInterrupt(digitalPinToInterrupt(encoder0PinB), doEncoderB, CHANGE);
//    attachInterrupt(digitalPinToInterrupt(encoder1PinA), doEncoderC, CHANGE);
//  attachInterrupt(digitalPinToInterrupt(encoder1PinB), doEncoderD, CHANGE);
  
//    attachInterrupt(digitalPinToInterrupt(greenECR), encoRA, CHANGE);
//  attachInterrupt(digitalPinToInterrupt(whiteECR), encoRB, CHANGE);
//
//    attachInterrupt(digitalPinToInterrupt(greenECL), encoLA, CHANGE);
//  attachInterrupt(digitalPinToInterrupt(whiteECL), encoLB, CHANGE);

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("ABMY SYSTEM");
  lcd.setCursor(4, 1);
  lcd.print("BYWAHJOE");
  delay(2000);
  lcd.clear();
  
  // verify connection
  //Serial.println("Testing device connections...");
  //Serial.println(mag.testConnection() ? "HMC5883L connection successful" : "HMC5883L connection failed");
  now=millis();
  before=millis();
}

void loop() {
//Serial.print(pulseL);Serial.print(",");Serial.println(pulseR);
  pulseL=mLeft.read();
  pulseR=mRight.read();
  go.kompas=getKompas();
  go.rotationL=getPutaran(pulseL);
  go.rotationR=getPutaran(pulseR);
  go.vpulseL=pulseL;
  go.vpulseR=pulseR; 
  
  now=millis();
  if(now-before>=15L){
      Serial.write((byte*)&go,sizeof(go));
    }
  if(now-before>=50L){
    updateLCD();  
    before=millis();  
  }
//    Serial.println(go.kompas);
//    Serial.println(go.rotationL);
//    Serial.println(go.rotationR);
//    Serial.println(go.vpulseL);
//    Serial.println(go.vpulseR);



//  Serial.println("TEST");
//  int angle = getKompas();
//  Serial.println(angle);
  delay(15);
}
void updateLCD(){
  int rotateL=getPutaran(pulseL);
  int rotateR=getPutaran(pulseR);
  int angle=getKompas();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(rotateL);
  lcd.setCursor(7,0);
  lcd.print(angle);
  lcd.setCursor(12,0);
  lcd.print(rotateR);

  lcd.setCursor(0,1);
  lcd.print(pulseL);
  lcd.setCursor(8,1);
  lcd.print(pulseR);    
  
}
int getPutaran(long pulse){
  int result=pulse/majuR;
  return result;
  }
int getKompas() {
  mag.getHeading(&mx, &my, &mz);

  // display tab-separated gyro x/y/z values
  //Serial.print("mag:\t");
  //Serial.print(mx); Serial.print("\t");
  //Serial.print(my); Serial.print("\t");
  //Serial.print(mz); Serial.print("\t");

  // To calculate heading in degrees. 0 degree indicates North
  float heading = atan2(my, mx);
  if (heading < 0)heading += 2 * M_PI;
  //Serial.print("heading:\t");

  int angle = heading * 180 / M_PI;
  return angle;
}
void encoRA(){
  if (digitalRead(greenECR) == HIGH){
    if (digitalRead(whiteECR) == LOW){
      pulseR=pulseR-3;
    }
    else {
       pulseR=pulseR+1;
    }
  }
  else {
    if (digitalRead(greenECR) == HIGH) {
       pulseR=pulseR-3;; 
    }
    else { pulseR=pulseR+1;;    }
  }
}
void encoRB(){
  if (digitalRead(whiteECR) == HIGH){
    if (digitalRead(greenECR) == HIGH){
       pulseR=pulseR-3;
    }
    else {
       pulseR=pulseR+1;
    }
  }
  else {
    if (digitalRead(greenECR) == LOW) {
       pulseR=pulseR-3;; 
    }
    else { pulseR=pulseR+1;    }
  }
}
void encoLA(){
  if (digitalRead(greenECL) == HIGH){
    if (digitalRead(whiteECL) == LOW){
      pulseL=pulseL-3;
    }
    else {
       pulseL=pulseL+1;
    }
  }
  else {
    if (digitalRead(greenECL) == HIGH) {
       pulseL=pulseL-3;; 
    }
    else { pulseL=pulseL+1;;    }
  }
}
void encoLB(){
  if (digitalRead(whiteECL) == HIGH){
    if (digitalRead(greenECL) == HIGH){
       pulseL=pulseL-3;
    }
    else {
       pulseL=pulseL+1;
    }
  }
  else {
    if (digitalRead(greenECL) == LOW) {
       pulseL=pulseL-3; 
    }
    else { pulseL=pulseL+1;    }
  }
}

void doEncoderA(){
  if (digitalRead(encoder0PinA) == HIGH){
    if (digitalRead(encoder0PinB) == LOW){
      encoder0Pos = encoder0Pos - 1;
    }
    else {
      encoder0Pos = encoder0Pos + 1;
    }
  }
  else {
    if (digitalRead(encoder0PinB) == HIGH) {
      encoder0Pos = encoder0Pos - 1; 
    }
    else {
      encoder0Pos = encoder0Pos + 1;
    }
  }
}

void doEncoderB(){
  if (digitalRead(encoder0PinB) == HIGH){
    if (digitalRead(encoder0PinA) == HIGH){
      encoder0Pos = encoder0Pos - 1;
    }
    else {
      encoder0Pos = encoder0Pos + 1;
    }
  }
  else {
    if (digitalRead(encoder0PinA) == LOW) {
      encoder0Pos = encoder0Pos - 1; 
    }
    else {
      encoder0Pos = encoder0Pos + 1;
    }
  }
}

void doEncoderC(){
  if (digitalRead(encoder1PinA) == HIGH){
    if (digitalRead(encoder1PinB) == LOW){
      encoder1Pos = encoder1Pos + 1;
    }
    else {
      encoder1Pos = encoder1Pos - 1;
    }
  }
  else {
    if (digitalRead(encoder1PinB) == HIGH) {
      encoder1Pos = encoder1Pos + 1; 
    }
    else {
      encoder1Pos = encoder1Pos - 1;
    }
  }
}

void doEncoderD(){
  if (digitalRead(encoder1PinB) == HIGH){
    if (digitalRead(encoder1PinA) == HIGH){
      encoder1Pos = encoder1Pos + 1;
    }
    else {
      encoder1Pos = encoder1Pos - 1;
    }
  }
  else {
    if (digitalRead(encoder0PinA) == LOW) {
      encoder1Pos = encoder1Pos + 1; 
    }
    else {
      encoder1Pos = encoder1Pos - 1;
    }
  }
}
