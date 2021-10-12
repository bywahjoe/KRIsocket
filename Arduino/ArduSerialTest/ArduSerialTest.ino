typedef struct 
{
  int32_t kompas;
  int32_t rotationL;
  int32_t rotationR;
  long pulseL;
  long pulseR;  

  
} mylog;

mylog go;
void setup() {
  // put your setup code here, to run once:
  randomSeed(analogRead(0));
  Serial.begin(9600);
}

void loop() {
  go.kompas=random(1,10);
  go.rotationL=random(10,20);
  go.rotationR=random(20,30);
  go.pulseL=random(-30,-10);
  go.pulseR=random(-40,-10); 

 Serial.write((byte*)&go,sizeof(go));
// Serial.println(sizeof(go));
// Serial.println(sizeof(go));
 delay(250);
}
