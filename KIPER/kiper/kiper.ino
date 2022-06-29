#include <EEPROM.h>
#include "pinku.h"
#include <LiquidCrystal_I2C.h>
#include <Encoder.h>

#define startBTN digitalRead(buttonStart)
#define calibBTN digitalRead(buttonCalib)

Encoder encoMotorA(motorEncoderA1, motorEncoderA2);
Encoder encoMotorB(motorEncoderB1, motorEncoderB2);

LiquidCrystal_I2C lcd(0x27, 20, 4);

struct sensor {
  unsigned int valSensor[8];
  unsigned int minSensor[8];
  unsigned int maxSensor[8];
  unsigned int centerSensor[8];
};
sensor left;
sensor right;
byte addrsLeft = 0; //Address EEPROM
byte addrsRight = 130;
byte sizee = 300;

bool multiplex[8][3] = {
  {0, 1, 0}, //C2 - [0]
  {0, 0, 1}, //C1 - [1]
  {0, 0, 0}, //C0 - [2]
  {0, 1, 1}, //C3 - [3]
  {1, 0, 0}, //C4 - [4]
  {1, 1, 0}, //C6 - [5]
  {1, 1, 1}, //C7 - [6]
  {1, 0, 1}, //C5 - [7]

};
byte noLine[] = {
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111
};
byte inLine[] = {
  B00000,
  B00000,
  B00000,
  B00000,
  B00000,
  B00000,
  B11111,
  B11111
};
byte verif[8] = {
  B00000,
  B00001,
  B00011,
  B10110,
  B11100,
  B01000,
  B00000,
  B00000
};

unsigned long nows = 0, before = 0;
bool white = 1, green = 0;
int valMax = 4095;
int valMin = 0;

char useSensor = 'L';
char msg[4] = {'L', 'C', 'R','M'};
char ballPos = 'C';
int index1 = 0;

float rotateppr = 540;
float diameter = 9.5;
int pulseA = 0, pulseB = 0;
const int freq = 1000;
const int reso = 8;

//----------PID---------------//
int errorL = 0;
int lastErrorL = 0;
int errorR = 0;
int lastErrorR = 0;

byte kp = 3;
byte kd = 1;
byte SPEED = 50;
int MIN_SPEED = -60;
byte MAX_SPEED = 75;
//----------------------------//
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  EEPROM.begin(500);

  //Button
  pinMode(buttonStart, INPUT_PULLUP);
  pinMode(buttonCalib, INPUT_PULLUP);

  //Multiplex
  pinMode(sensorR0, OUTPUT);
  pinMode(sensorR1, OUTPUT);
  pinMode(sensorR2, OUTPUT);
  pinMode(sensorL0, OUTPUT);
  pinMode(sensorL1, OUTPUT);
  pinMode(sensorL2, OUTPUT);

  //MTR
  ledcSetup(1, freq, reso);
  ledcSetup(2, freq, reso);
  ledcSetup(3, freq, reso);
  ledcSetup(4, freq, reso);

  ledcAttachPin(motorA1, 1);
  ledcAttachPin(motorA2, 2);
  ledcAttachPin(motorB1, 3);
  ledcAttachPin(motorB2, 4);

  //IR
  pinMode(leftIR, INPUT);
  pinMode(rightIR, INPUT);

  //LCD
  lcd.init();
  lcd.clear();
  lcd.backlight();
  lcd.createChar(0, noLine);
  lcd.createChar(1, inLine);
  lcd.createChar(2, verif);

  readCenterEEPROM();
  welcome();

  nows = millis();
  before = millis();
  delay(1000);
  //  motionStart();

  //  while (1);

}

void loop() {
  // put your main code here, to run repeatedly:
  pulseA = encoMotorA.read();
  pulseB = encoMotorB.read();

  readLineSensor();

  //  Serial.println(calibBTN);
  if (Serial.available() > 0) {
    char recv = Serial.read();
    ballPos = recv;
    if (ballPos == 'L')setSensor('L');
    else if (ballPos == 'R')setSensor('R');
    else {}
  }

  if (!calibBTN) {
    robotCalib();
  }
  if (!startBTN) {
    setMotor(0, 0);
    lcd.clear();

    ballPos = msg[index1];
    if (ballPos != 'C' && ballPos!='M') setSensor(ballPos);
    lcd.print(ballPos);

    index1++;
    if (index1 > 3)index1 = 0;
    delay(1000);
  }

  if (ballPos == 'L') {
    if (getLeftIR())setMotor(0, 0);
    else {
      followLine();
    }
  }
  else if (ballPos == 'R') {
    if (getRightIR())setMotor(0, 0);
    else {
      followLine();
    }
  } else if (ballPos == 'C') setMotor(0, 0);
  else if (ballPos == 'M') motionStart();

  //  for(int i=0;i<8;i++){
  //    Serial.print(getRightSensor(i));Serial.print(",");
  //
  //    }
  //  Serial.println();
  //  delay(200);

  //Timer LCD
  nows = millis();
  if (nows - before > 200UL) {
    displayLCD();
    before = nows;
  }
}
void setSensor(char selectSensor) {
  useSensor = selectSensor;
}
void welcome() {
  lcd.clear();
  lcd.setCursor(4, 1);
  lcd.print("ABMY SYSTEM"); lcd.write(2);
  lcd.setCursor(6, 2);
  lcd.print("BYWAHJOE");
  lcd.setCursor(0, 3);
  delay(1000);

  for (int i = 0; i < 20; i++) {
    lcd.write(0);
    delay(100);
  }
  lcd.clear();
}
void readCenterEEPROM() {
  EEPROM.get(addrsLeft, left);
  EEPROM.get(addrsRight, right);
  /*
  for (int i = 0; i < 8; i++) {
    Serial.print(left.valSensor[i]); Serial.print(",");
  }
  Serial.println();

  for (int i = 0; i < 8; i++) {
    Serial.print(left.minSensor[i]); Serial.print(",");
  }
  Serial.println();

  for (int i = 0; i < 8; i++) {
    Serial.print(left.maxSensor[i]); Serial.print(",");
  }
  Serial.println();

  for (int i = 0; i < 8; i++) {
    Serial.print(left.centerSensor[i]); Serial.print(",");
  }
  Serial.println();

  for (int i = 0; i < 8; i++) {
    Serial.print(right.valSensor[i]); Serial.print(",");
  }
  Serial.println();

  for (int i = 0; i < 8; i++) {
    Serial.print(right.minSensor[i]); Serial.print(",");
  }
  Serial.println();

  for (int i = 0; i < 8; i++) {
    Serial.print(right.maxSensor[i]); Serial.print(",");
  }
  Serial.println();

  for (int i = 0; i < 8; i++) {
    Serial.print(right.centerSensor[i]); Serial.print(",");
  }
  Serial.println();
  */
}
void robotCalib() {
  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.print("Starting Calibrate..");
  delay(2000);
  lcd.setCursor(0, 1);
  lcd.print("Ready Calibrate.....");
  resetMinMaxSensor();

  while (calibBTN) {
    for (int i = 0; i < 8; i++)setCenterSensor(i);
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Writing Memory..");

  EEPROM.put(addrsLeft, left);
  bool saveLeft = EEPROM.commit();
  EEPROM.put(addrsRight, right);
  bool saveRight = EEPROM.commit();

  //  Serial.println(left.centerSensor[0]);
  lcd.setCursor(0, 1);
  for (int i = 0; i < 20; i++) {
    lcd.write(0);
    delay(100);
  }

  lcd.setCursor(0, 2);
  if (saveLeft && saveRight)lcd.print("DONE OK...");
  else lcd.print("Failed");
  delay(2000);

}
void resetMinMaxSensor() {
  for (int i = 0; i < 8; i++) {
    left.minSensor[i] = valMax;
    left.maxSensor[i] = valMin;
    right.minSensor[i] = valMax;
    right.maxSensor[i] = valMin;
  }
}
void setCenterSensor(int chnl) {
  int valL, valR;
  valL = getLeftSensor(chnl);
  if (valL > left.maxSensor[chnl])left.maxSensor[chnl] = valL;
  if (valL < left.minSensor[chnl])left.minSensor[chnl] = valL;

  valR = getRightSensor(chnl);
  if (valR > right.maxSensor[chnl])right.maxSensor[chnl] = valR;
  if (valR < right.minSensor[chnl])right.minSensor[chnl] = valR;

  left.centerSensor[chnl] = (left.maxSensor[chnl] + left.minSensor[chnl]) / 2;
  right.centerSensor[chnl] = (right.maxSensor[chnl] + right.minSensor[chnl]) / 2;
}
bool getLineDisplay(int chnl, char selectSensor) {
  bool result = white;
  if (selectSensor == 'L') {
    if (left.valSensor[chnl] < left.centerSensor[chnl]) result = white;
    else result = green;
  }
  else {
    if (right.valSensor[chnl] < right.centerSensor[chnl]) result = white;
    else result = green;
  }
  return result;
}
void readLineSensor() {
  for (int i = 0; i < 8; i++) {
    left.valSensor[i] = getLeftSensor(i);
    right.valSensor[i] = getRightSensor(i);
  }
}
int sensorToByte(char selectSensor) {
  int b = 1;
  int result = 0;

  if (selectSensor == 'L') {
    for (int i = 0; i < 8; i++) {
      result += getLineDisplay(i, selectSensor) * b;
      b *= 2;
    }
  }
  else {
    for (int i = 0; i < 8; i++) {
      result += getLineDisplay(i, selectSensor) * b;
      b *= 2;
    }
  }
  return result;
}
void followLine() {
  readLineSensor();
  int mysensorL = sensorToByte('L');
  int mysensorR = sensorToByte('R');

  switch (mysensorL) {
    case 0b00000001: errorL = -7;  break;
    case 0b00000011: errorL = -6;  break;
    case 0b00000111: errorL = -5;  break;
    case 0b00001111: errorL = -4;  break;
    case 0b00011111: errorL = -3;  break;
    case 0b00111111: errorL = -2;  break;
    case 0b00111110: errorL = -1;  break;
    case 0b01111110: errorL = 0;  break;
    case 0b01111100: errorL = 1;  break;
    case 0b11111100: errorL = 2;  break;
    case 0b11111000: errorL = 3;  break;
    case 0b11110000: errorL = 4;  break;
    case 0b11100000: errorL = 5;  break;
    case 0b11000000: errorL = 6;  break;
    case 0b10000000: errorL = 7;  break;  
  }
  switch (mysensorR) {
    case 0b00000001: errorR = -7;  break;
    case 0b00000011: errorR = -6;  break;
    case 0b00000111: errorR = -5;  break;
    case 0b00001111: errorR = -4;  break;
    case 0b00011111: errorR = -3;  break;
    case 0b00111111: errorR = -2;  break;
    case 0b00111110: errorR = -1;  break;
    case 0b01111110: errorR = 0;  break;
    case 0b01111100: errorR = 1;  break;
    case 0b11111100: errorR = 2;  break;
    case 0b11111000: errorR = 3;  break;
    case 0b11110000: errorR = 4;  break;
    case 0b11100000: errorR = 5;  break;
    case 0b11000000: errorR = 6;  break;
    case 0b10000000: errorR = 7;  break; 
  }

  int rateError, error;

  if (useSensor == 'L') {
    rateError = errorL - lastErrorL;
    error = errorL; //--
    //      Serial.println(mysensorL,BIN);
  } else {
    rateError = errorR - lastErrorR;
    error = errorR; //--
    //          Serial.println(mysensorR,BIN);
  }

  lastErrorL = errorL;
  lastErrorR = errorR;
  int moveVal = (int)(error * kp) + (rateError * kd);

  int moveLeft = SPEED + moveVal;
  int moveRight = SPEED - moveVal;

  moveLeft = constrain(moveLeft, MIN_SPEED, MAX_SPEED);
  moveRight = constrain(moveRight, MIN_SPEED, MAX_SPEED);
  //  Serial.print(moveLeft); Serial.print(","); Serial.println(moveRight);
  //Bawah,Atas
  //
  //  setMotor(moveLeft,moveRight);
  //
  if (useSensor == 'L')  setMotor(-moveRight, -moveLeft);
  else { //Atas Bawah
    setMotor(moveLeft, moveRight);
  }
}
float getRotate(int pulse) {
  float result = pulse / rotateppr;
  return result;

}
bool getLeftIR() {
  int mysensor = digitalRead(leftIR);
  return !mysensor;
}
bool getRightIR() {
  int mysensor = digitalRead(rightIR);
  return !mysensor;
}

int getRightSensor(int chnl) {
  digitalWrite(sensorR0, multiplex[chnl][2]);
  digitalWrite(sensorR1, multiplex[chnl][1]);
  digitalWrite(sensorR2, multiplex[chnl][0]);
  int val = analogRead(sensorROut);
  return val;
}
int getLeftSensor(int chnl) {
  digitalWrite(sensorL0, multiplex[chnl][2]);
  digitalWrite(sensorL1, multiplex[chnl][1]);
  digitalWrite(sensorL2, multiplex[chnl][0]);
  int val = analogRead(sensorLOut);
  return val;
}
void displayLCD() {
  lcd.clear();

  //Left Sensor Display
  lcd.setCursor(0, 0);
  for (int i = 0; i < 8; i++)lcd.write(getLineDisplay(i, 'L'));

  //Right Sensor Display
  lcd.setCursor(0, 3);
  for (int i = 7; i >= 0; i--)lcd.write(getLineDisplay(i, 'R'));

  lcd.setCursor(9, 0);
  lcd.print("POS:"); lcd.print(ballPos);
  lcd.setCursor(15, 0);
  lcd.print("RUN:"); lcd.print(useSensor);
  lcd.setCursor(9, 1);
  lcd.print("E-A:"); lcd.print(pulseA);
  lcd.setCursor(9, 2);
  lcd.print("E-B:"); lcd.print(pulseB);

  lcd.setCursor(9, 3);
  lcd.print(getRotate(pulseA));
  lcd.print(",");
  lcd.print(getRotate(pulseB));

  lcd.setCursor(0, 1);
  lcd.print("IRL:"); lcd.print(getLeftIR());
  lcd.setCursor(0, 2);
  lcd.print("IRR:"); lcd.print(getRightIR());

}
void setMotor(int speedA, int speedB) {
  if (speedA > 0) {
    ledcWrite(1, speedA);
    ledcWrite(2, 0);
  } else {
    speedA = speedA * -1;
    ledcWrite(1, 0);
    ledcWrite(2, speedA);
  }

  if (speedB > 0) {
    ledcWrite(3, speedB);
    ledcWrite(4, 0);
  } else {
    speedB = speedB * -1;
    ledcWrite(3, 0);
    ledcWrite(4, speedB);
  }
}
void rem() {
  setMotor(0, 0);

}
void remDelay(int timex) {
  rem();
  delay(timex);

}
void resetEncoder() {
  encoMotorA.write(0);
  encoMotorB.write(0);
}
void moveTo(float distanceCM, int myspeed, int err) {
  rem();
  resetEncoder();
  float avgPulse = 0.0, result = 0.0;
  int valECA, valECB;


  bool forward = true;
  float circumference = PI * diameter;

  if (distanceCM < 0) {
    myspeed = myspeed * -1;
    setMotor(myspeed, myspeed);
    err = err * -1;
    forward = false;

  } else {
    setMotor(myspeed, myspeed);
  }

  while (1) {
    int speedA = myspeed, speedB = myspeed;
    valECA = encoMotorA.read();
    valECB = encoMotorB.read();
    avgPulse = (valECA + valECB) / 2;
    result = (avgPulse / 480) * circumference;

    if (valECA > valECB)speedB + err;
    else if (valECB > valECA)speedA + err;

    if (forward && result > distanceCM)break;
    else if (!forward && result < distanceCM) break;
    setMotor(speedA, speedB);
  };
  lcd.setCursor(0, 2);
  lcd.print(result); lcd.print("             ");
  remDelay(1000);
}
void turnTo(int angle, int myspeed) {
  // use wheel encoders to pivot (turn) by specified angle

  // set motor power for pivoting
  int power = myspeed; // clockwise

  // use correction to improve angle accuracy
  // adjust correction value based on test results
  float correction = -10.0; // need decimal point for float value
  if (angle > 0) angle += correction;
  else if (angle < 0) angle -= correction;

  // variable for tracking wheel encoder counts
  long rightCount = 0;

  // values based on RedBot's encoders, motors & wheels
  float countsPerRev = 480.0; // 192 encoder ticks per wheel revolution
  float wheelDiam = diameter; // wheel diameter = 65 mm = 2.56 in
  float wheelCirc = PI * wheelDiam; // wheel circumference = 3.14 x 2.56 in = 8.04 in
  float pivotDiam = 38.0; // pivot diameter = distance between centers of wheel treads = 6.125 in
  float pivotCirc = PI * pivotDiam; // pivot circumference = 3.14 x 6.125 in = 19.23 in

  // based on angle, calculate distance (arc length) for pivot
  float distance = abs(angle) / 360.0 * pivotCirc;

  // based on distance, calculate number of wheel revolutions
  float numRev = distance / wheelCirc;

  // based on number of revolutions, calculate target encoder count
  float targetCount = numRev * countsPerRev;

  // reset encoder counters and start pivoting
  resetEncoder();
  //delay(100);
  if (angle < 0) {
    setMotor(-power, power);
  } else {
    setMotor(power, -power);
  }

  // keeps looping while right encoder count less than target count
  while (abs(rightCount) < abs(targetCount)) {
    // get current wheel encoder count
    rightCount =   encoMotorB.read();
    //delay(10);  // short delay before next reading
  }

  // target count reached
  rem();
  delay(1000);
}
void followSEC(int secondx){
  unsigned long stopx=millis()+secondx;
  while(millis()<stopx)followLine(); //MAJU MILLIS
  }
void motionStart() {
  
  lastErrorL=0,lastErrorR=0;
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("MOTION START");
  setSensor('R');
  delay(3000);
  followSEC(500);
  
  while(1){
    followLine();
    if(!getLineDisplay(0, 'R')&&getLineDisplay(4, 'R')&&getLineDisplay(5, 'R') && getLineDisplay(6, 'R') &&getLineDisplay(7, 'R')) break;
    }
    remDelay(500);
 
    setMotor(50,50);
    while(1){
      readLineSensor();
      delay(100);
     if(!getLineDisplay(5, 'R') && !getLineDisplay(6, 'R') && !getLineDisplay(7, 'R'))break;
      
      }
  
  remDelay(500);
  
  setMotor(50,-50);
  while(!getLineDisplay(5, 'R')) readLineSensor(); //RIGHT

  followSEC(2000);  
  remDelay(1000);
  /*
  moveTo(107, 50, 50);
  turnTo(90, 50);
  moveTo(93, 50, 50)*/
  turnTo(60, 50);
  lastErrorL=0,lastErrorR=0;
  
  while (1) {
//    readLineSensor();
    followLine();
    //    for (int i = 0; i < 8; i++) {
    //      Serial.print(getLineDisplay(i, 'R'));
    //
    //      Serial.println("");
    //    }
    if (getLineDisplay(2, 'R') == 1 || getLineDisplay(3, 'R') == 1)break;
  }
  remDelay(1000);
  setMotor(50, 50); delay(300); //Go
  remDelay(500);
  setMotor(-50, 50);
  while (!getLineDisplay(2, 'R'))readLineSensor();
  rem();

  ballPos = 'R';
  setSensor(ballPos);

}
