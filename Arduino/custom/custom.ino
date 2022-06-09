#include "Wire.h"
#include "I2Cdev.h"
#include "HMC5883L.h"
#include <Encoder.h>
#include <LiquidCrystal_I2C.h>
#include "math.h"

#define buzz A10
#define buzzON digitalWrite(buzz,HIGH)
#define buzzOFF digitalWrite(buzz,LOW)

Encoder mLeft(19, 18);
Encoder mRight(3, 2);

LiquidCrystal_I2C lcd(0x27, 16, 2);
HMC5883L mag;
int sensiKompas=2; //Sensi

int16_t mx, my, mz;
float majuR = 2400.0;
long pulseL = 0, pulseR = 0;

//Timer
unsigned long now, before;
unsigned long myTimer = 100;

typedef struct
{
  int32_t kompas;
  float rotationL;
  float rotationR;
  long vpulseL;
  long vpulseR;
} mylog;
float lastRotationL = 0, lastRotationR = 0;
int32_t lastKompas = 0;
mylog go;

bool kompasChange = false;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pinMode(buzz, OUTPUT);
  //  Serial.println("OK");
  mag.initialize();

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
  now = millis();
  before = millis();
  while (Serial.available());
}

void loop() {
  //Serial.print(pulseL);Serial.print(",");Serial.println(pulseR);

  pulseL = mLeft.read();
  pulseR = mRight.read();
  go.kompas = getKompas();
  go.rotationL = getPutaran(pulseL);
  go.rotationR = getPutaran(pulseR);

  go.vpulseL = pulseL;
  go.vpulseR = pulseR;

//Serial.println(go.rotationL);
  //Kompas +1 0 -1
  if (lastKompas >= go.kompas - sensiKompas && lastKompas <= go.kompas + sensiKompas )kompasChange = false;
  else {
    kompasChange = true;
  };

  //Send Msg
  if (lastRotationL != go.rotationL || lastRotationR != go.rotationR || kompasChange == true) {
    Serial.write((byte*)&go, sizeof(go));
    lastRotationL = go.rotationL;
    lastRotationR = go.rotationR;
    lastKompas = go.kompas;
    buzzON;
    delay(100);
    buzzOFF;

    //    Serial.begin(9600);
  }

  //LCD Interval Update
  now = millis();
  if (now - before >= myTimer) {
    updateLCD();
    before = millis();
    //    Serial.flush();
  }

  //    Serial.println(go.kompas);
  //    Serial.println(go.rotationL);
  //    Serial.println(go.rotationR);
  //    Serial.println(go.vpulseL);
  //    Serial.println(go.vpulseR);

}
void updateLCD() {
  float rotateL = getPutaran(pulseL);
  float rotateR = getPutaran(pulseR);
  int angle = getKompas();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(rotateL);
  lcd.setCursor(7, 0);
  lcd.print(angle);
  lcd.setCursor(11, 0);
  lcd.print(rotateR);

  lcd.setCursor(0, 1);
  lcd.print(pulseL);
  lcd.setCursor(8, 1);
  lcd.print(pulseR);

}
float getPutaran(long pulse) {
  float result = pulse / majuR;
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