#include "Wire.h"
#include "I2Cdev.h"
#include "HMC5883L.h"

HMC5883L mag;

int16_t mx, my, mz;

void setup() {
  Wire.begin();
  Serial.begin(38400);

  mag.initialize();

  // verify connection
  //Serial.println("Testing device connections...");
  //Serial.println(mag.testConnection() ? "HMC5883L connection successful" : "HMC5883L connection failed");
}

void loop() {
  int angle = getKompas();
  Serial.println(angle);
  delay(200);
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
